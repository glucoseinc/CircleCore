import CCAPI from './api'

const TOKEN_KEY = 'crcr:session'
const CLIENT_ID = '8F9A5449-F219-4BC4-9EA6-5F4C3100CD25'
const CLIENT_SECRET = (
  '3f82ad86ff167cebc39bf735533efe080b596f4ce343e4f51fd6c760a9835ccb' +
  '6ff76df5d2e72489b30d07ce81a273a6ea4128f98412f4b6027245c76cd0a098'
)

/**
 * CRCR用のOAuthToken
 */
class OAuthToken {
  /**
   * @constructor
   * @param {string} storage storage
   * @param {string} storageKey storageKey
   * @param {string} clientID clientID
   * @param {string} clientSecret clientSecret
   * @param {string} accessToken accessToken
   * @param {string} refreshToken refreshToken
   */
  constructor(storage, storageKey, clientID, clientSecret, accessToken, refreshToken) {
    this._storage = storage
    this._storageKey = storageKey
    this.clientID = clientID,
    this.clientSecret = clientSecret
    this.accessToken = accessToken
    this.refreshToken = refreshToken
  }

  /**
   * tokenをストレージから読み込む
   * @return {bool} 読み込めればtrue, 読み込めなければfalse
   */
  load() {
    let raw = this._storage.getItem(this._storageKey)
    if(!raw)
      return false

    let [accessToken, refreshToken] = raw.split(':')
    this.update(accessToken, refreshToken)
    return true
  }

  /**
   * tokenをストレージに保存する
   */
  save() {
    this._storage.setItem(
      this._storageKey,
      `${encodeURIComponent(this.accessToken)}:${encodeURIComponent(this.refreshToken)}`
    )
  }

  /**
   * tokenをクリアし、ストレージからも消す
   */
  clear() {
    this.accessToken = null
    this.refreshToken = null
    this._storage.removeItem(this._storageKey)
  }

  /**
   * OAuthTokenが設定されているか確認（現在有効化どうかは確認しない）
   * @return {bool} acess & refresh tokenが有効そうに見えるならTrue
   */
  isValid() {
    return this.accessToken && this.accessToken.length && this.refreshToken && this.refreshToken.length ? true : false
  }

  /**
   * tokenを更新する
   * @param {string} accessToken 新しいAccess Token
   * @param {string} refreshToken 新しいRefresh Token
   */
  update(accessToken, refreshToken) {
    this.accessToken = accessToken
    this.refreshToken = refreshToken
  }
}

export let oauthToken = new OAuthToken(localStorage, TOKEN_KEY, CLIENT_ID, CLIENT_SECRET)


/**
 * ログアウトする。画面遷移あり
 */
export async function logout() {
  try {
    await CCAPI.revokeToken()
  } catch(e) {
    // pass error
  }
  oauthToken.clear()
  location.href = '/'
}


/**
 * ?key=val&key=val 形式のクエリをParseする
 * @param {string} queryString クエリ文字列
 * @return {Object} Parse済クエリ
 */
function _parseQuery(queryString) {
  let query = {}
  queryString.forEach((part) => {
    let pos = part.indexOf('=')
    if(pos >= 0) {
      query[decodeURIComponent(part.substr(0, pos))] = decodeURIComponent(part.substr(pos + 1))
    } else {
      query[decodeURIComponent(part)] = null
    }
  })
  return query
}


/**
 * AuthorizationCodeが返ってきているかどうかをチェックする
 * @param {str} hash '#xxxxx'
 * @return {bool} AuthCodeが返ってきている
 */
export function checkHasAuthCodeReceived(hash) {
  if(!hash.startsWith('#')) {
    // invalid hash string
    return null
  }

  let query = _parseQuery(hash.substr(1).split('&'))
  if(query.access_token) {
    // unsupported
    return null
  } else if(query.code) {
    return query.code
  }

  return null
}


/**
 * 受け取ったauthorization codeをtokenに変える
 * @param {string} authorizationCode AuthorizationCode
 * @return {Object} accessToken, refreshToken
 */
export async function fetchTokenByAuthorizationCode(authorizationCode) {
  let response
  try {
    response = await CCAPI.oauthToken({
      grant_type: 'authorization_code',
      code: authorizationCode,
      redirect_uri: `${location.origin}/oauth/callback`,
      client_id: CLIENT_ID,
    })

    if(response.token_type != 'Bearer') {
      throw new Error('unknown token type')
    }
  } catch(e) {
    // failed to get token
    return null
  }

  let {access_token, refresh_token} = response
  return {
    accessToken: access_token,
    refreshToken: refresh_token,
  }
}


// 認証開始URL
export const OAUTH_AUTHORIZATION_URL = `/oauth/authorize?client_id=${CLIENT_ID}&response_type=code`
