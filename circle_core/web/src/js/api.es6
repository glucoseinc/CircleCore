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
          // 全体に向けてToken無効化Actionを発行する
          const {actionTypes} = require('src/actions')
          const {store} = require('src/main')

          store.dispatch({
            type: actionTypes.auth.tokenInvalidated,
          })

          // もとのAPI呼び出し元にもエラーを伝える
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


  // Invitation
  /**
   * Invitationを作成する
   * @param {object} rawInvitation
   * @return {object} Result
   */
  async createInvitation(rawInvitation) {
    const res = await this._post('/invitations/', rawInvitation)
    return res.body
  }

  /**
   * Invitationの詳細を得る
   * @param {string} invitationId
   * @return {object} Result
   */
  async fetchInvitation(invitationId) {
    const res = await this._get(`/invitations/${invitationId}`)
    return res.body
  }

  /**
   * Invitationのリストを得る
   * @return {object} Result
   */
  async fetchAllInvitations() {
    const res = await this._get('/invitations/')
    return res.body
  }

  /**
   * Invitationを削除する
   * @param {string} invitationId
   * @return {object} Result
   */
  async deleteInvitation(invitationId) {
    const res = await this._delete(`/invitations/${invitationId}`)
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
   * Userを作成する
   * @param {object} rawUser
   * @return {object} Result
   */
  async createUser(rawUser) {
    const res = await this._post('/users/', rawUser)
    return res.body
  }

  /**
   * Userの詳細を得る
   * @param {string} userId
   * @return {object} Result
   */
  async fetchUser(userId) {
    const res = await this._get(`/users/${userId}`)
    return res.body
  }

  /**
   * Userのリストを得る
   * @return {object} Result
   */
  async fetchAllUsersNew() {
    const res = await this._get('/users/')
    return res.body
  }

  /**
   * 自分自身の詳細を得る
   * @return {object} Result
   */
  async fetchMyselfUser() {
    const res = await this._get('/users/me')
    return res.body
  }

  /**
   * Userを更新する
   * @param {object} rawUser
   * @return {object} Result
   */
  async updateUser(rawUser) {
    const res = await this._put(`/users/${rawUser.uuid}`, rawUser)
    return res.body
  }

  /**
   * Userを削除する
   * @param {string} userId
   * @return {object} Result
   */
  async deleteUser(userId) {
    const res = await this._delete(`/users/${userId}`)
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

  /**
   * MessageBoxの最新データを得る
   * @param {string} moduleId
   * @param {string} messageBoxId
   * @return {object} Result
   */
  async fetchLatestMessageBox(moduleId, messageBoxId) {
    const res = await this._get(`/modules/${moduleId}/${messageBoxId}/data?format=json&limit=5`)
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

  /**
   * CircleCoreInfoを更新する
   * @param {object} rawCcInfo
   * @return {object} Result
   */
  async updateCcInfo(rawCcInfo) {
    const res = await this._put(`/cores/${rawCcInfo.uuid}`, rawCcInfo)
    return res.body
  }


  // ReplicationLink
  /**
   * ReplicationLinkを作成する
   * @param {object} rawReplicationLink
   * @return {object} Result
   */
  async createReplicationLink(rawReplicationLink) {
    const res = await this._post('/replicas/', rawReplicationLink)
    return res.body
  }

  /**
   * ReplicationLinkの詳細を得る
   * @param {string} replicationLinkId
   * @return {object} Result
   */
  async fetchReplicationLink(replicationLinkId) {
    const res = await this._get(`/replicas/${replicationLinkId}`)
    return res.body
  }

  /**
   * ReplicationLinkのリストを得る
   * @return {object} Result
   */
  async fetchAllReplicationLinks() {
    const res = await this._get('/replicas/')
    return res.body
  }

  /**
   * ReplicationLinkを削除する
   * @param {string} replicationLinkId
   * @return {object} Result
   */
  async deleteReplicationLink(replicationLinkId) {
    const res = await this._delete(`/replicas/${replicationLinkId}`)
    return res.body
  }

  /**
   * ReplicationMasterのリストを得る
   * @return {object} Result
   */
  async fetchAllReplicationMasters() {
    const res = await this._get('/replication_masters/')
    return res.body
  }

  /**
   * ReplicationMasterを削除する
   * @param {string} replicationMasterId
   * @return {object} Result
   */
  async deleteReplicationMaster(replicationMasterId) {
    const res = await this._delete(`/replication_masters/${replicationMasterId}`)
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
