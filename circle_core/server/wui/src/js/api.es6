import request from 'superagent'

import Schema from './models/Schema'
import SchemaPropertyType from './models/SchemaPropertyType'
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
   * @param {Schema} schema Schema
   * @return {Schema} Schema
   */
  async getSchema(schema) {
    const res = await this._get(`/schemas/${schema.uuid}`)
    return Schema.fromObject(res.body.schema)
  }

  /**
   * Schemaを作成する
   * @param {Schema} schema Schema
   * @return {Object} Result
   */
  async postSchema(schema) {
    const res = await this._post('/schemas/', schema.toJS())
    return res.body
  }

  /**
   * Schemaを削除する
   * @param {Schema} schema Schema
   * @return {Object} Result
   */
  async deleteSchema(schema) {
    const res = await this._delete(`/schemas/${schema.uuid}`)
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
   * @param {Module} module Module
   * @return {Module} Module
   */
  async getModule(module) {
    const res = await this._get(`/modules/${module.uuid}`)
    return res.body
  }

  /**
   * Moduleを作成する
   * @param {Module} module Module
   * @return {Object} Result
   */
  async postModule(module) {
    const res = await this._post('/modules/', module.toJS())
    return res.body
  }


  /**
   * Moduleを削除する
   * @param {Module} module Module
   * @return {Object} Result
   */
  async deleteModule(module) {
    const res = await this._delete(`/modules/${module.uuid}`)
    return res.body
  }
}


export default new CCAPI('/api')
