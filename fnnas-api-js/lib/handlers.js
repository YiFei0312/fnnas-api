const { aes_decrypt } = require('./encryption');
const { BadRequestError } = require('./exceptions');

async function HandlerDefault(client, data) {
  if ("errno" in data) {
    const error_code = data["errno"];
    throw new BadRequestError(error_code, data);
  }
}

async function HandlerGetRSAPub(client, data) {
  client.pub = data.pub || null;
  client.si = data.si || null;
}

async function HandlerLogin(client, data) {
  client.backId = data.backId || null;
  client.token = data.token || null;
  client.secret = data.secret || null;
  client.uid = data.uid || null;
  client.admin = data.admin || null;
  client.sign_key = aes_decrypt(client.secret, client.key, client.iv);
}

async function HandlerUserInfo(client, data) {
  // 以下是用户详细回调函数
}

async function HandlerGetSI(client, data) {
  client.si = data.si || null;
}

async function HandlerAuthToken(client, data) {
}

async function HandlerFileList(client, data) {
  console.log(data);
}

class AsyncFileEventHandler {
  constructor(queue, loop) {
    this.queue = queue;
    this.loop = loop;
  }

  on_modified(event) {
    if (!event.is_directory) {
      this.queue.put_nowait(['modified', event.src_path]);
    }
  }

  on_created(event) {
    if (!event.is_directory) {
      this.queue.put_nowait(['created', event.src_path]);
    }
  }

  on_deleted(event) {
    if (!event.is_directory) {
      this.queue.put_nowait(['deleted', event.src_path]);
    }
  }
}

module.exports = {
  HandlerDefault,
  HandlerGetRSAPub,
  HandlerLogin,
  HandlerUserInfo,
  HandlerGetSI,
  HandlerAuthToken,
  HandlerFileList,
  AsyncFileEventHandler
};