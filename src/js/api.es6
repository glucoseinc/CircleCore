import request from 'superagent'


/**
 * CircleCore管理用APIのラッパ
 */
class CCAPI {
  /**
   * @constructor
   * @param {String} prefix API endpoint
   */
  constructor(prefix) {
    this.prefixer = require('superagent-prefix')(prefix)
  }

  /**
   * GETクエリを発行する
   * @param {String} path APIのパス
   * @param {Object} [query] クエリ
   * @return {Object} 戻り値
   */
  _get(path, query) {
    return request
      .get(path)
      .use(this.prefixer)
      .set('Accept', 'application/json')
      // .withCredentials()
      .query(query || {})
  }


  // modules
  /**
   * モジュールのリストを得る
   * @return {Array<Module>} モジュールのリスト
   */
  async listModules() {
    let res = await this._get('/modules/')
    return res.body
  }

  /**
   * モジュールの詳細を得る
   * @param {String} moduleId モジュールのID
   * @return {Module} モジュール
   */
  async getModule(moduleId) {
    let res = await this._get(`/modules/${moduleId}`)
    return res.body
  }
}


export default new CCAPI('/api')
