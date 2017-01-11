import request from 'superagent'

import Schema, {SchemaPropertyType} from './models/Schema'
import Module from './models/Module'

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

  /**
   * POSTクエリを発行する
   * @param {String} path APIのパス
   * @param {Object} [params] パラメータ
   * @return {Object} 戻り値
   */
  _post(path, params) {
    return request
      .post(path)
      .use(this.prefixer)
      .set('Accept', 'application/json')
      // .withCredentials()
      .send(params || {})
  }

  /**
   * DELETEクエリを発行する
   * @param {String} path APIのパス
   * @param {Object} [query] クエリ
   * @return {Object} 戻り値
   */
  _delete(path, query) {
    return request
    .del(path)
    .use(this.prefixer)
    .set('Accept', 'application/json')
    // .withCredentials()
    .query(query || {})
  }


  // schemas
  /**
   * Schemaのリストを得る
   * @return {Array<Schema>} Schemaのリスト
   */
  async getSchemas() {
    const res = await this._get('/schemas/')
    return res.body.schemas.map(Schema.fromObject)
  }

  /**
   * Schemaの詳細を得る
   * @param {String} schemaId SchemaのID
   * @return {Schema} Schema
   */
  async getSchema(schemaId) {
    let res = await this._get(`/schemas/${schemaId}`)
    return res.body
  }

  /**
   * Schemaを作成する
   * @param {Object} [schema] パラメータ
   * @return {Object} Result
   */
  async postSchema(schema) {
    const res = await this._post('/schemas/', schema)
    return res.body
  }

  /**
   * Schemaを削除する
   * @param {String} schemaId SchemaのID
   * @return {Object} Result
   */
  async deleteSchema(schemaId) {
    const res = await this._delete(`/schemas/${schemaId}`)
    return res.body
  }

  /**
   * Schema Property Typeのリストを得る
   * @return {Array<Schema>} Schema Property Typeのリスト
   */
  async getSchemaPropertyTypes() {
    const res = await this._get('/schemas/propertytypes')
    return res.body.propertyTypes.map(SchemaPropertyType.fromObject)
  }

  // modules
  /**
   * Moduleのリストを得る
   * @return {Array<Module>} モジュールのリスト
   */
  async getModules() {
    const res = await this._get('/modules/')
    return res.body.modules.map(Module.fromObject)
  }

  /**
   * Moduleの詳細を得る
   * @param {String} moduleId モジュールのID
   * @return {Module} モジュール
   */
  async getModule(moduleId) {
    let res = await this._get(`/modules/${moduleId}`)
    return res.body
  }

  /**
   * Moduleを削除する
   * @param {String} moduleId ModuleのID
   * @return {Object} Result
   */
  async deleteModule(moduleId) {
    const res = await this._delete(`/modules/${moduleId}`)
    return res.body
  }
}


export default new CCAPI('/api')
