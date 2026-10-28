const WebSocket = require('ws');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const http = require('http');
const https = require('https');
const { WebSocketConnectionError } = require('./exceptions');
const { get_reqid, generate_random_string } = require('./utils');
const { login_encrypt, get_signature_req, get_signature } = require('./encryption');
const { HandlerDefault, HandlerGetRSAPub, HandlerLogin, HandlerGetSI, HandlerAuthToken } = require('./handlers');

class BaseClient {
  constructor(ping_interval = 30, logger = null) {
    this.websocket = null;
    this.handlers = {};
    this.pending_requests = {};
    this.req_mapping = {};
    this.ping_interval = ping_interval;

    this._listen_task = null;
    this._ping_task = null;
    this.__url = null;

    this.sign_key = null;
    this.key = generate_random_string(32);
    this.iv = crypto.randomBytes(16);

    this.si = null;
    this.pub = null;
    this.backId = '0000000000000000';
    this.token = null;
    this.secret = null;
    this.uid = null;
    this.admin = null;

    if (!logger) {
      this.logger = {
        debug: (msg) => console.log(`[DEBUG] ${msg}`),
        info: (msg) => console.log(`[INFO] ${msg}`),
        error: (msg) => console.error(`[ERROR] ${msg}`),
        exception: (err) => console.error(`[EXCEPTION] ${err}`)
      };
    } else {
      this.logger = logger;
    }
  }

  async connected() {
    if (!this.websocket || this.websocket.readyState !== WebSocket.OPEN) {
      return false;
    }
    try {
      return true;
    } catch (error) {
      return false;
    }
  }

  async _init(...args) {
    throw new Error("子类必须实现 _init 方法");
  }

  async connect(url = null, ...args) {
    if (url !== null) {
      this.__url = url;
    }
    try {
      this.websocket = new WebSocket(this.__url);
      await new Promise((resolve, reject) => {
        this.websocket.on('open', resolve);
        this.websocket.on('error', reject);
      });

      this._listen();
      this._ping_loop();

      await this._init(...args);
    } catch (error) {
      throw new WebSocketConnectionError(`Failed to connect: ${error.message}`);
    }
  }

  _listen() {
    this.websocket.on('message', async (message) => {
      try {
        const data = JSON.parse(message);
        this.logger.debug(`Received: ${message}`);
        if ('reqid' in data) {
          const reqid = data['reqid'];
          if (reqid in this.pending_requests) {
            const handler = this.pending_requests[reqid];
            delete this.pending_requests[reqid];
            handler(data);
          }
          if (reqid in this.req_mapping) {
            const req_type = this.req_mapping[reqid];
            delete this.req_mapping[reqid];
            const handler = this.handlers[req_type] || HandlerDefault;
            await handler(this, data);
          }
        }
      } catch (error) {
        this.logger.exception(error);
      }
    });

    this.websocket.on('close', () => {
      this.logger.debug('Websocket connection closed');
    });

    this.websocket.on('error', (error) => {
      this.logger.exception(error);
    });
  }

  _ping_loop() {
    const pingInterval = setInterval(async () => {
      try {
        await this.send_ping();
      } catch (error) {
        this.logger.error(`Failed to send ping: ${error.message}`);
        clearInterval(pingInterval);
        await this.connect();
      }
    }, this.ping_interval * 1000);
    this._ping_task = pingInterval;
  }

  async send_ping() {
    try {
      this.websocket.send(JSON.stringify({ "req": "ping" }));
      this.logger.debug("Sent ping to server");
    } catch (error) {
      this.logger.error(`Failed to send ping: ${error.message}`);
      throw error;
    }
  }

  async send_request(req, ...kwargs) {
    const reqid = get_reqid(this.backId);
    const data = { 'req': req, 'reqid': reqid, ...kwargs[0] };
    if (req === 'user.login' || req === 'user.add') {
      const dataStr = JSON.stringify(data).replace(/\s/g, '');
      const encryptedData = login_encrypt(dataStr, this.pub, this.key, this.iv);
      const message = get_signature_req(encryptedData, this.sign_key);
      this.websocket.send(message);
      this.req_mapping[reqid] = req;
      this.logger.debug(`Sent: ${req} ${message}`);
      return reqid;
    }
    const message = get_signature_req(data, this.sign_key);
    this.websocket.send(message);
    this.req_mapping[reqid] = req;
    this.logger.debug(`Sent: ${req} ${message}`);
    return reqid;
  }

  add_handler(req, handler) {
    this.handlers[req] = handler;
  }

  async request(req, ...kwargs) {
    const reqid = await this.send_request(req, ...kwargs);
    return new Promise((resolve) => {
      this.pending_requests[reqid] = (data) => resolve(data);
    });
  }

  async close(timeout = 5.0) {
    if (this._ping_task) {
      clearInterval(this._ping_task);
    }
    if (this.websocket) {
      this.websocket.close();
    }
    this.logger.info("Connection closed.");
  }

  run_polling({ stop_signals = null, close_timeout = 5.0 } = {}) {
    if (stop_signals === null) {
      stop_signals = ['SIGINT', 'SIGTERM'];
    }

    const _async_main = async () => {
      await this.connect();
      this.logger.info("Client started. Press Ctrl+C to stop...");
      await new Promise((resolve) => {
        const handleSignal = () => {
          resolve();
        };
        for (const sig of stop_signals) {
          process.on(sig, handleSignal);
        }
      });
      await this.close(timeout = close_timeout);
    };

    try {
      _async_main();
    } catch (error) {
      this.logger.info("User interrupted, shutting down...");
    } finally {
      this.logger.info("Client stopped.");
    }
  }
}

class MainClient extends BaseClient {
  async _init() {
    this.add_handler('util.crypto.getRSAPub', HandlerGetRSAPub);
    this.add_handler('user.login', HandlerLogin);
    await this.request('util.crypto.getRSAPub');
  }

  async login(username, password, { deviceType = 'Browser', deviceName = 'Windows-Google Chrome', stay = false } = {}) {
    const data = {
      "user": username,
      "password": password,
      "deviceType": deviceType,
      "deviceName": deviceName,
      "stay": stay,
      "si": this.si
    };
    const response = await this.request('user.login', data);
    return response;
  }

  async user_info() {
    const response = await this.request('user.info');
    return response;
  }

  async setting_port({ force_https = false, redirect = true, http_port = 5666, https_port = 5667 } = {}) {
    const data = {
      "data": {
        "force_https": force_https,
        "redirect": redirect,
        "schema": {
          "http": {
            "port": http_port
          },
          "https": {
            "port": https_port
          }
        }
      }
    };
    const response = await this.request('appcgi.network.gw.setting', data);
    return response;
  }

  async get_user_storage() {
    const data = {
      "quotaInfo": true,
      "spaceInfo": true,
      "storInfo": true
    };
    const response = await this.request("stor.getUserStorage", data);
    return response;
  }
}

class FileClient extends BaseClient {
  async _init() {
    this.add_handler('util.getSI', HandlerGetSI);
    this.add_handler('user.authToken', HandlerAuthToken);
    this.file_update_queue = [];
    this._update_file();
  }

  async getSI() {
    await this.request('util.getSI');
  }

  async authToken() {
    await this.getSI();
    const data = {
      "si": this.si,
      "token": this.token,
    };
    await this.request('user.authToken', data);
  }

  async fileList(path = null) {
    const data = {
      "path": path,
    };
    return await this.request('file.ls', data);
  }

  async upload(local_path, nas_path, overwrite = 2) {
    const nasPathObj = path.parse(nas_path);
    const folder = nasPathObj.dir;
    const file_name = nasPathObj.base;
    const mtim = Math.floor(fs.statSync(local_path).mtimeMs / 1000).toString();
    const res = await this._checkUpload(local_path, nas_path, overwrite);
    const uploadName = res.uploadName;

    const url = 'http://192.168.1.143:5666/upload';
    const headers = {
      'Referer': 'http://192.1688.143:5666/p/assets/upload.worker-CPfLJtMs.js',
      'Trim-Overwrite': overwrite.toString(),
      'Trim-Token': this.token,
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
      'Accept': 'application/json, text/plain, */*',
      'Trim-Mtim': mtim,
      'Trim-Path': `${folder}/${uploadName}`,
    };
    headers['Trim-Sign'] = get_signature(headers['Trim-Path'], this.sign_key);

    const fileContent = fs.readFileSync(local_path);
    const mime_type = this._guessMimeType(local_path);

    const boundary = '----WebKitFormBoundary' + Math.random().toString(36).substring(2);
    const body = this._buildFormData(file_name, fileContent, mime_type, boundary);

    headers['Content-Type'] = `multipart/form-data; boundary=${boundary}`;
    headers['Content-Length'] = Buffer.byteLength(body);

    return new Promise((resolve, reject) => {
      const req = http.request(url, { method: 'POST', headers }, (res) => {
        let data = '';
        res.on('data', (chunk) => data += chunk);
        res.on('end', () => resolve({ statusCode: res.statusCode, data }));
      });
      req.on('error', (error) => reject(error));
      req.write(body);
      req.end();
    });
  }

  _guessMimeType(filePath) {
    const ext = path.extname(filePath).toLowerCase();
    const mimeTypes = {
      '.txt': 'text/plain',
      '.html': 'text/html',
      '.css': 'text/css',
      '.js': 'application/javascript',
      '.json': 'application/json',
      '.xml': 'application/xml',
      '.jpg': 'image/jpeg',
      '.jpeg': 'image/jpeg',
      '.png': 'image/png',
      '.gif': 'image/gif',
      '.pdf': 'application/pdf',
      '.zip': 'application/zip',
      '.rar': 'application/x-rar-compressed',
      '.7z': 'application/x-7z-compressed',
      '.exe': 'application/x-msdownload',
      '.dll': 'application/x-msdownload',
      '.mp3': 'audio/mpeg',
      '.mp4': 'video/mp4',
      '.avi': 'video/x-msvideo',
      '.mov': 'video/quicktime',
      '.wmv': 'video/x-ms-wmv',
      '.doc': 'application/msword',
      '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      '.xls': 'application/vnd.ms-excel',
      '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      '.ppt': 'application/vnd.ms-powerpoint',
      '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
    };
    return mimeTypes[ext] || 'application/octet-stream';
  }

  _buildFormData(fileName, fileContent, mimeType, boundary) {
    let formData = `--${boundary}\r\n`;
    formData += `Content-Disposition: form-data; name="trim-upload-file"; filename="${fileName}"\r\n`;
    formData += `Content-Type: ${mimeType}\r\n\r\n`;
    formData += fileContent.toString('binary');
    formData += `\r\n--${boundary}--`;
    return formData;
  }

  async download() {
    // http://192.168.1.4:5666/multiple-download?token=0
  }

  async _checkUpload(local_path, nas_path, overwrite = 2) {
    const size = fs.statSync(local_path).size;
    const data = {
      "size": size,
      "path": nas_path,
      "overwrite": overwrite,
    };
    const res = await this.request('file.checkUpload', data);
    return res;
  }

  async _update_file() {
    while (true) {
      if (this.file_update_queue.length > 0) {
        const [local_path, nas_path, action] = this.file_update_queue.shift();
        console.log(local_path, nas_path, action);
        if (action === 'u') {
          await this.upload(local_path, nas_path, 1);
        } else if (action === 'd') {
          await this.download();
        }
      }
      await new Promise(resolve => setTimeout(resolve, 100));
    }
  }

  async start_observer({ nas_path = null, local_path = process.cwd(), recursive = false, interval = 5, exclude = null } = {}) {
    if (exclude === null) {
      exclude = [];
    }
    while (true) {
      const res = await this.fileList({ path: nas_path });
      const nas_files = res.files || [];
      const nas_dict = {};
      for (const file of nas_files) {
        nas_dict[file.name] = file.mtim;
      }
      const local_files = {};
      const local_path_dict = {};
      for (const [name, file_path, mtime] of this._list_files(local_path, recursive)) {
        if (exclude.includes(name)) {
          continue;
        }
        local_files[name] = mtime;
        local_path_dict[name] = file_path;
      }
      for (const [name, nas_mtim] of Object.entries(nas_dict)) {
        if (name in local_files) {
          const local_mtim = local_files[name];
          if (nas_mtim > local_mtim) {
            console.log(`文件 '${name}' 在NAS上较新，更新到本地。`);
            this.file_update_queue.push([local_path_dict[name], `${nas_path}/${name}`, 'd']);
          } else if (nas_mtim < local_mtim) {
            console.log(`文件 '${name}' 在本地较新，更新到NAS。`);
            console.log(name, nas_mtim, local_mtim);
            this.file_update_queue.push([local_path_dict[name], `${nas_path}/${name}`, 'u']);
          }
        } else {
          console.log(`本地不存在文件 '${name}'，从NAS复制到本地。`);
          this.file_update_queue.push([`${local_path}/${name}`, `${nas_path}/${name}`, 'd']);
        }
      }
      for (const name of Object.keys(local_files)) {
        if (!(name in nas_dict)) {
          console.log(`NAS不存在文件 '${name}'，从本地复制到NAS。`);
          this.file_update_queue.push([local_path_dict[name], `${nas_path}/${name}`, 'u']);
        }
      }
      await new Promise(resolve => setTimeout(resolve, interval * 1000));
    }
  }

  *_list_files(dir, recursive = false) {
    const files = fs.readdirSync(dir);
    for (const file of files) {
      const fullPath = path.join(dir, file);
      const stats = fs.statSync(fullPath);
      if (stats.isDirectory()) {
        if (recursive) {
          yield* this._list_files(fullPath, recursive);
        }
      } else {
        const mtime = Math.floor(stats.mtimeMs / 1000);
        yield [file, fullPath, mtime];
      }
    }
  }

  async file_search(key, path) {
    const data = {
      "key": key,
      "path": path,
    };
    const res = await this.request("appcgi.finder.fileSearch", data);
    return res;
  }
}

class EmptyClient extends BaseClient {
  async _init() {
  }
}

class FnOsClient extends FileClient {
  async _init() {
    this.add_handler('util.crypto.getRSAPub', HandlerGetRSAPub);
    this.add_handler('user.login', HandlerLogin);
    await this.request('util.crypto.getRSAPub');
  }

  async login(username, password, { deviceType = 'Browser', deviceName = 'Windows-Google Chrome', stay = false } = {}) {
    const data = {
      "user": username,
      "password": password,
      "deviceType": deviceType,
      "deviceName": deviceName,
      "stay": stay,
      "si": this.si
    };
    const response = await this.request('user.login', data);
    return response;
  }

  async user_info() {
    const response = await this.request('user.info');
    return response;
  }

  async setting_port({ force_https = false, redirect = true, http_port = 5666, https_port = 5667 } = {}) {
    const data = {
      "data": {
        "force_https": force_https,
        "redirect": redirect,
        "schema": {
          "http": {
            "port": http_port
          },
          "https": {
            "port": https_port
          }
        }
      }
    };
    const response = await this.request('appcgi.network.gw.setting', data);
    return response;
  }

  async get_user_storage() {
    const data = {
      "quotaInfo": true,
      "spaceInfo": true,
      "storInfo": true
    };
    const response = await this.request("stor.getUserStorage", data);
    return response;
  }
}

module.exports = {
  FnOsClient,
  MainClient,
  FileClient,
  EmptyClient
};