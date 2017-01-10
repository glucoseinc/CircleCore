import CCAPI from './api'

const TOKEN_KEY = 'crcr:session'
const CLIENT_ID = '8F9A5449-F219-4BC4-9EA6-5F4C3100CD25'
const CLIENT_SECRET = '3f82ad86ff167cebc39bf735533efe080b596f4ce343e4f51fd6c760a9835ccb6ff76df5d2e72489b30d07ce81a273a6ea4128f98412f4b6027245c76cd0a098'


/**
 * CRCR用のOAuthToken
 */
class OAuthToken {
  /**
   * @constructor
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

  load() {
    let raw = this._storage.getItem(this._storageKey)
    if(!raw)
      return false

    let [accessToken, refreshToken] = raw.split(':')
    this.update(accessToken, refreshToken)
    return true
  }

  save() {
    this._storage.setItem(
      this._storageKey,
      `${encodeURIComponent(this.accessToken)}:${encodeURIComponent(this.refreshToken)}`
    )
  }

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
    return this.accessToken && this.accessToken.length && this.refreshToken && this.refreshToken.length
  }

  update(accessToken, refreshToken) {
    this.accessToken = accessToken
    this.refreshToken = refreshToken
  }
}

var oauthToken = new OAuthToken(localStorage, TOKEN_KEY, CLIENT_ID, CLIENT_SECRET)


/**
 * 認証系をチェックして必要な動作を行う
 *
 * A. access_tokenがある → Tokenの死活チェック
 * B. access_tokenがない →
 *    B-1. 返りfragmentにcodeがある → codeの確認
 *    B-2. ない → 認証フロー開始
 */
export async function checkAuthorization() {
  CCAPI.setToken(oauthToken)

  if(oauthToken.load()) {
    // tokenがある -> 死活チェック(...はしない、API使った時の認証エラーでなんとかすればええねん)

    // token tests
    // try{let resp = await CCAPI._get('/oauth/scope_test/user');     console.log(resp)} catch(e) {console.log('failed')}
    // try{let resp = await CCAPI._get('/oauth/scope_test/schema+r');     console.log(resp)} catch(e) {console.log('failed')}
    // try{let resp = await CCAPI._get('/oauth/scope_test/schema+rw');     console.log(resp)} catch(e) {console.log('failed')}
    // try{let resp = await CCAPI._get('/oauth/scope_test/bad-scope');     console.log(resp)} catch(e) {console.log('failed')}

    return true
  } else {
    // tokenがない ->

    // authorization codeを受け取っている最中である
    let authCode = _checkHasAuthCodeReceived()

    // clear hash
    location.hash = ''

    if(authCode) {
      // authCodeの死活チェック
      let tokenData = await _checkAuthorizationCode(authCode)
      if(tokenData) {
        let {accessToken, refreshToken} = tokenData
        oauthToken.update(accessToken, refreshToken)
        oauthToken.save()
        return true
      }
    }
  }

  // ここまで来たら、ログインしていないこと確定なので、ログインしていただく
  _startAuthorization()
  return false
}

export async function logout() {
  try {
    await CCAPI.revokeToken()
  } catch(e) {
  }
  oauthToken.clear()
  location.href = '/'
}

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


function _checkHasAuthCodeReceived() {
  const hash = location.hash

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


async function _checkAuthorizationCode(authorizationCode) {
  let response
  try {
    response = await CCAPI.oauthToken({
      grant_type: 'authorization_code',
      code: authorizationCode,
      redirect_uri: `${location.origin}`,
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


function _startAuthorization() {
  let url = `/oauth/authorize?client_id=${CLIENT_ID}&response_type=code`

  location.href = url
}

