const fs = require('fs');
const path = require('path');
const { BadRequestError } = require('./exceptions');

function _get_reqid() {
  let index = 1;

  return function(backId = '0000000000000000') {
    const t = Math.floor(Date.now() / 1000).toString(16).padStart(8, '0');
    const e = index.toString(16).padStart(4, '0');
    index += 1;
    return `${t}${backId}${e}`;
  };
}

const get_reqid = _get_reqid();

function generate_random_string(t) {
  const chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
  let result = '';
  for (let i = 0; i < t; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

function check_response(response) {
  if ("errno" in response) {
    const error_code = response["errno"];
    throw new BadRequestError(error_code, response);
  }
}

function get_mtime(path) {
  const stats = fs.statSync(path);
  return Math.floor(stats.mtimeMs / 1000);
}

function* list_files(dir, recursive = false) {
  const files = fs.readdirSync(dir);
  for (const file of files) {
    const fullPath = path.join(dir, file);
    const stats = fs.statSync(fullPath);
    if (stats.isDirectory()) {
      if (recursive) {
        yield* list_files(fullPath, recursive);
      }
    } else {
      const mtime = get_mtime(fullPath);
      yield [file, fullPath, mtime];
    }
  }
}

module.exports = {
  get_reqid,
  generate_random_string,
  check_response,
  get_mtime,
  list_files
};