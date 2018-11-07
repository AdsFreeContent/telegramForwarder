const request = require('request')
const AGENT_URL = require('../config/agent').url;

const _sendRequest = (endpoint) => {
  return new Promise((resolve, reject) => {
    request(AGENT_URL + endpoint, { json: true }, (err, resp, body) => {
      if (err) return reject(err);
      return resolve(body);
    })
  })
}

class ForwardAgent {

  static async joinPublicEntity(entityName) {
    const endpoint = `joinPublicEntity?entity=${entityName}`;
    try {
      const resp = await _sendRequest(endpoint);
      return resp;
    } catch (err) {
      return err;
    }
  }

  static async joinPrivateEntity(hash) {
    const endpoint = `joinPrivateEntity?hash=${hash}`;
    try {
      const resp = await _sendRequest(endpoint);
      return resp;
    } catch (err) {
      return err;
    }
  }

  static async getEntity(entity) {
    const endpoint = `getentity?entity=${entity}`;
    try {
      const resp = await _sendRequest(endpoint);
      return resp;
    } catch (err) {
      return err;
    }
  }

}

module.exports = ForwardAgent;
