import request from 'superagent'

import Invitation from './models/Invitation'
import User from './models/User'


/**
 * superagentのリクエストをリセットする
 * @param {object} req リクエスト
 * @return {object} リセットされたRequest
 */
function resetRequest(req) {
  // superagentをhackしているのでversionによっては動かなくなると思う
  delete req._callback
  delete req.xhr
  delete req._fullfilledPromise
  delete req._endCalled
  return req
}


/**
 * API呼び出し用の便利クラス
 */
class APICaller {
  /**
   * @constructor
   * @param {String} prefix API endpoint
   */
  constructor(prefix) {
    this.prefixer = require('superagent-prefix')(prefix)
    this.token = null
  }

  /**
   * OAuty用のTokenを設定する
   * @param {OAuthToken} token OAuth token
   */
  setToken(token) {
    this.token = token
  }

  /**
   * GETクエリを発行する
   * @param {String} path APIのパス
   * @param {Object} [query] クエリ
   * @return {Object} 戻り値
   */
  _get(path, query) {
    return this._wrapRequestWithAuthorization(request
      .get(path)
      .use(this.prefixer)
      .set('Accept', 'application/json')
      .query(query || {})
    )
  }

  /**
   * POSTクエリを発行する
   * @param {String} path APIのパス
   * @param {Object} [params] パラメータ
   * @return {Object} 戻り値
   */
  _post(path, params) {
    return this._wrapRequestWithAuthorization(request
      .post(path)
      .use(this.prefixer)
      .set('Accept', 'application/json')
      .send(params || {})
    )
  }

  /**
   * PUTクエリを発行する
   * @param {String} path APIのパス
   * @param {Object} [params] パラメータ
   * @return {Object} 戻り値
   */
  _put(path, params) {
    return this._wrapRequestWithAuthorization(request
      .put(path)
      .use(this.prefixer)
      .set('Accept', 'application/json')
      .send(params || {})
    )
  }

  /**
   * DELETEクエリを発行する
   * @param {String} path APIのパス
   * @param {Object} [query] クエリ
   * @return {Object} 戻り値
   */
  _delete(path, query) {
    return this._wrapRequestWithAuthorization(request
      .del(path)
      .use(this.prefixer)
      .set('Accept', 'application/json')
      .query(query || {})
    )
  }

  /**
   * リクエストを認証付きで発行する。TokenRefreshが必要であればやり直す
   * @param {req} req req
   * @return {Promise} リクエストの返り値を渡すPromise
   */
  async _wrapRequestWithAuthorization(req) {
    require('assert')(this.token.accessToken)

    req = req.set('Authorization', `Bearer ${this.token.accessToken}`)

    try {
      return await req
    } catch(err) {
      if(err.status == 403) {
        // refresh token, and retry
        await this._extendToken()

        // retry
        req = resetRequest(req).set('Authorization', `Bearer ${this.token.accessToken}`)
        return await req
      }
      throw err
    }
  }

  /**
   * tokenを更新する
   * ref 18.2.4
   * @return {Promise} リクエストのPromise
   */
  _extendToken() {
    if(this._extendTokenRequest) {
      // extend中
      console.log('extending... suspend request')
      return this._extendTokenRequest
    }

    // create new request
    this._extendTokenRequest = new Promise((resolve, reject) => {
      this._requestRefresh()
        .then((res) => {
          // succeeded
          console.log('refresh token', res.body)

          this.token.update(res.body.access_token, res.body.refresh_token)
          this.token.save()

          delete this._extendTokenRequest
          resolve()
        }, (err) => {
          // rejected
          console.log('extend failed!')
          reject(err)
        })
    })
    return this._extendTokenRequest
  }

  /**
   * Tokenを更新する
   * @return {Promise} 更新完了したら呼ばれるRefresh
   */
  _requestRefresh() {
    /* eslint-disable camelcase */
    return request
      .post('/oauth/token')
      .type('form')
      .set('Accept', 'application/json')
      .send({
        grant_type: 'refresh_token',
        client_id: this.token.clientID,
        // client_secret: this.token.clientSecret,
        refresh_token: this.token.refreshToken,
      })
    /* eslint-enable camelcase */
  }
}


/**
 * CircleCore管理用APIのラッパ
 */
class CCAPI extends APICaller {
  // auth
  /**
   * oauthでもらったcodeからtokenを得る
   * @param {Object} query query
   * @return {Object} token?
   */
  async oauthToken(query) {
    // form-url-encodedで送らないといけないので...
    let res = await request.post('/oauth/token')
      .type('form')
      .set('Accept', 'application/json')
      .send(query)
    return res.body
  }

  /**
   * oauthでもらったcodeからtokenを得る
   * @return {object} token?
   */
  async revokeToken() {
    // form-url-encodedで送らないといけないので...
    let res = await request.get('/oauth/revoke')
      .set('Accept', 'application/json')
    return res.body
  }

  // invitation
  /**
   * Invitationのリストを得る
   * @return {List<Invitation>} Result
   */
  async listInvitations() {
    const res = await this._get('/invitations/')
    return res.body.invitations.map(Invitation.fromObject)
  }

  /**
   * Invitationを作成する
   * @param {Object} payload 新しく作りたいInvitationの値
   * @return {Object} Result
   */
  async postInvitation(payload) {
    const res = await this._post('/invitations/', payload)
    return Invitation.fromObject(res.body.response)
  }

  /**
   * Invitationを削除する
   * @param {Invitation} invitation Invtation
   * @return {Object} Result
   */
  async deleteInvitation(invitation) {
    const res = await this._delete(`/invitations/${invitation.uuid}`)
    return res.body.invitation
  }


  // schemas
  /**
   * Schemaのリストを得る
   * @return {Array<Schema>} Schemaのリスト
   */
  async getSchemas() {
    const res = await this._get('/schemas/')
    return res.body
  }

  /**
   * Schemaの詳細を得る
   * @param {Schema} schema Schema
   * @return {Schema} Schema
   */
  async getSchema(schema) {
    const res = await this._get(`/schemas/${schema.uuid}`)
    return res.body
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
    return res.body
  }

  // users
  /**
   * Userのリストを得る
   * @return {Array<User>} Userのリスト
   */
  async getUsers() {
    const res = await this._get('/users/')
    return res.body.users.map(User.fromObject)
  }

  /**
   * Userを削除する
   * @param {User} user User
   * @return {Object} Result
   */
  async deleteUser(user) {
    const res = await this._delete(`/users/${user.uuid}`)
    return res.body
  }

  // modules
  /**
   * Moduleのリストを得る
   * @return {Array<Module>} モジュールのリスト
   */
  async getModules() {
    const res = await this._get('/modules/')
    return res.body
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
   * Moduleを更新する
   * @param {Module} module Module
   * @return {Object} Result
   */
  async putModule(module) {
    const res = await this._put(`/modules/${module.uuid}`, module.toJS())
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
