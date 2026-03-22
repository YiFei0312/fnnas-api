const crypto = require('crypto');
const fs = require('fs');

function generate_random_string(t) {
  const chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
  let result = '';
  for (let i = 0; i < t; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

function rsa_encrypt(public_key_str, plaintext) {
  const publicKey = crypto.createPublicKey(public_key_str);
  const encrypted = crypto.publicEncrypt(
    {
      key: publicKey,
      padding: crypto.constants.RSA_PKCS1_PADDING
    },
    Buffer.from(plaintext, 'utf8')
  );
  return encrypted.toString('base64');
}

function aes_encrypt(data, key, iv) {
  const cipher = crypto.createCipheriv('aes-256-cbc', Buffer.from(key), iv);
  let encrypted = cipher.update(data, 'utf8', 'base64');
  encrypted += cipher.final('base64');
  return encrypted;
}

function unpkcs7(buffer) {
  const padLength = buffer[buffer.length - 1];
  if (padLength < 1 || padLength > 16) {
    return buffer;
  }
  return buffer.slice(0, buffer.length - padLength);
}

function aes_decrypt(ciphertext, key, iv) {
  const decipher = crypto.createDecipheriv('aes-256-cbc', Buffer.from(key), iv);
  decipher.setAutoPadding(false);
  const decrypted = Buffer.concat([
    decipher.update(Buffer.from(ciphertext, 'base64')),
    decipher.final()
  ]);
  
  const unpadded = unpkcs7(decrypted);
  return unpadded.toString('base64');
}

function login_encrypt(data, public_key_str, key, iv) {
  const rsa_encrypted = rsa_encrypt(public_key_str, key);
  const aes_encrypted = aes_encrypt(data, key, iv);

  return {
    'req': 'encrypted',
    'iv': iv.toString('base64'),
    'rsa': rsa_encrypted,
    'aes': aes_encrypted
  };
}

function get_signature(data, key) {
  const key_bytes = Buffer.from(key, 'base64');
  const hmac = crypto.createHmac('sha256', key_bytes);
  hmac.update(data, 'utf8');
  return hmac.digest('base64');
}

function get_signature_req(data, key) {
  const sign_req = [
    'encrypted',
    'util.getSI',
    'util.crypto.getRSAPub',
  ];
  const req = data['req'];
  const json_str = JSON.stringify(data).replace(/\s/g, '');
  if (!sign_req.includes(req)) {
    if (key) {
      return get_signature(json_str, key) + json_str;
    } else {
      return '' + json_str;
    }
  }
  return json_str;
}

module.exports = {
  generate_random_string,
  rsa_encrypt,
  aes_encrypt,
  aes_decrypt,
  login_encrypt,
  get_signature,
  get_signature_req
};