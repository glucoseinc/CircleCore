import request from 'superagent'


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
  listModules() {
    return this._get('modules')
  }

  /**
   * モジュールの詳細を得る
   * @return {Module} モジュール
   */
  getModule(moduleId) {
    return this._get(`modules/${moduleId}`)
  }
}


export default new CCAPI('/api/')
