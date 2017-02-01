import request from 'superagent'


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
      return this._extendTokenRequest
    }

    // create new request
    this._extendTokenRequest = new Promise((resolve, reject) => {
      this._requestRefresh()
        .then((res) => {
          // succeeded
          this.token.update(res.body.access_token, res.body.refresh_token)
          this.token.save()

          delete this._extendTokenRequest
          resolve()
        }, (err) => {
          // rejected
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
   * @return {Object} Result
   */
  async listInvitations() {
    const res = await this._get('/invitations/')
    return res.body
  }

  /**
   * Invitationを作成する
   * @param {Object} payload 新しく作りたいInvitationの値
   * @return {Object} Result
   */
  async postInvitation(payload) {
    const res = await this._post('/invitations/', payload)
    return res.body
  }

  /**
   * Invitationを削除する
   * @param {Invitation} invitation Invtation
   * @return {Object} Result
   */
  async deleteInvitation(invitation) {
    const res = await this._delete(`/invitations/${invitation.uuid}`)
    return res.body
  }


  // Schema
  /**
   * Schemaを作成する
   * @param {object} rawSchema
   * @return {object} Result
   */
  async createSchema(rawSchema) {
    const res = await this._post('/schemas/', rawSchema)
    return res.body
  }

  /**
   * Schemaの詳細を得る
   * @param {string} schemaId
   * @return {object} Result
   */
  async fetchSchema(schemaId) {
    const res = await this._get(`/schemas/${schemaId}`)
    return res.body
  }

  /**
   * Schemaのリストを得る
   * @return {object} Result
   */
  async fetchAllSchemas() {
    const res = await this._get('/schemas/')
    return res.body
  }

  /**
   * Schemaを削除する
   * @param {string} schemaId
   * @return {object} Result
   */
  async deleteSchema(schemaId) {
    const res = await this._delete(`/schemas/${schemaId}`)
    return res.body
  }


  // SchemaPropertyType
  /**
   * Schema Property Typeのリストを得る
   * @return {object} Result
   */
  async fetchAllSchemaPropertyTypes() {
    const res = await this._get('/schemas/propertytypes')
    return res.body
  }


  // User
  /**
   * Userのリストを得る
   * @return {Object} Userのリスト
   */
  async listUsers() {
    const res = await this._get('/users/')
    return res.body
  }

  /**
   * 特定Userを得る
   * @param {str} userId
   * @return {Object} Userのリスト
   */
  async getUser(userId) {
    const res = await this._get(`/users/${userId}`)
    return res.body
  }

  /**
   * ログインしている自分の情報を得る
   * @return {Object} Userのリスト
   */
  async getMe() {
    return this.getUser('me')
  }

  /**
   * Userを更新する
   * @param {Object} payload 更新データ Userオブジェクトではないことに注意
   * @return {Object} Result
   */
  async updateUser(payload) {
    const res = await this._put(`/users/${payload.uuid}`, payload)
    return res.body
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


  // Module
  /**
   * Moduleを作成する
   * @param {object} rawModule
   * @return {object} Result
   */
  async createModule(rawModule) {
    const res = await this._post('/modules/', rawModule)
    return res.body
  }

  /**
   * Moduleの詳細を得る
   * @param {string} moduleId
   * @return {object} Result
   */
  async fetchModule(moduleId) {
    const res = await this._get(`/modules/${moduleId}`)
    return res.body
  }

  /**
   * Moduleのリストを得る
   * @return {object} Result
   */
  async fetchAllModules() {
    const res = await this._get('/modules/')
    return res.body
  }

  /**
   * Moduleを更新する
   * @param {object} rawModule
   * @return {object} Result
   */
  async updateModule(rawModule) {
    const res = await this._put(`/modules/${rawModule.uuid}`, rawModule)
    return res.body
  }

  /**
   * Moduleを削除する
   * @param {string} moduleId
   * @return {object} Result
   */
  async deleteModule(moduleId) {
    const res = await this._delete(`/modules/${moduleId}`)
    return res.body
  }

  // CcInfo
  /**
   * CircleCoreInfoのリストを得る
   * @return {object} Result
   */
  async fetchAllCcInfos() {
    const res = await this._get('/cores/')
    return res.body
  }

  /**
   * 自身のCircleCoreInfoを得る
   * @return {object} Result
   */
  async fetchMyselfCcInfo() {
    const res = await this._get('/cores/myself')
    return res.body
  }

  // ModuleGraphData
  /**
   * Moduleのグラフ用データを得る
   * @param {Module} module Module
   * @param {object} query query
   * @return {object} グラフデータ
   */
  async getModuleGraphData(module, query) {
    const res = await this._get(`/modules/${module.uuid}/graph`, query)
    return res.body
  }


  // MessageBoxGraphData
  /**
   * MessageBoxのグラフ用データを得る
   * @param {Module} module Module
   * @param {MessageBox} messageBox Module
   * @param {object} query query
   * @return {object} グラフデータ
   */
  async getMessageBoxGraphData(module, messageBox, query) {
    const res = await this._get(`/modules/${module.uuid}/${messageBox.uuid}/graph`, query)
    return res.body
  }
}


export default new CCAPI('/api')
