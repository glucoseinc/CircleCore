/* eslint-disable new-cap */
import {Record} from 'immutable'
import moment from 'moment'


const UserRecord = Record({
  uuid: '',
  account: '',
  work: '',
  telephone: '',
  mailAddress: '',
  permissions: [],
  token: null,
  _createdAt: null,
  _updatedAt: null,
  _lastAccessAt: null,
})

/**
 * Userモデル
 */
export default class User extends UserRecord {
  /**
   * @override
   */
  constructor(...args) {
    super(...args)
  }

  /**
   * @param {object} rawUser
   * @return {User}
   */
  static fromObject(rawUser) {
    return new User({
      uuid: rawUser.uuid,
      account: rawUser.account,
      work: rawUser.work,
      telephone: rawUser.telephone,
      mailAddress: rawUser.mailAddress,
      permissions: rawUser.permissions,
      token: rawUser.token,
      _createdAt: moment.utc(rawUser.createdAt),
      _updatedAt: moment.utc(rawUser.updatedAt),
      _lastAccessAt: moment.utc(rawUser.lastAccessAt),
    })
  }

  /**
   * 表示用の名称
   * @return {string}
   */
  get displayName() {
    return this.account
  }

  /**
   * 管理者であるか？
   * @return {bool}
   */
  get isAdmin() {
    return this.permissions.indexOf('admin') >= 0
  }

  /**
   * 作成日時を返す
   * @return {string}
   */
  get createdAt() {
    return this._createdAt.isValid() ? this._createdAt.local().format('YY/MM/DD HH:mm') : ''
  }

  /**
   * 更新日時を返す
   * @return {string}
   */
  get updatedAt() {
    return this._updatedAt.isValid() ? this._updatedAt.local().format('YY/MM/DD HH:mm') : ''
  }

  /**
   * 最終ログイン日時を返す
   * @return {string}
   */
  get lastAccessAt() {
    return this._lastAccessAt.isValid() ? this._lastAccessAt.local().format('YY/MM/DD HH:mm') : ''
  }


  /**
   * @param {string} value
   * @return {User}
   */
  updateAccount(value) {
    return this.set('account', value)
  }

  /**
   * @param {string} value
   * @return {User}
   */
  updateDisplayName(value) {
    return this.updateAccount(value)
  }

  /**
   * @param {Boolean} value
   * @return {User}
   */
  updateIsAdmin(value) {
    const {permissions} = this
    const key = 'admin'
    const pos = permissions.indexOf(key)

    if (value) {
      // push admin
      if (pos <= 0) {
        permissions.push(key)
      }
    } else {
      // pop admin
      if (pos >= 0) {
        permissions.splice(pos, 1)
      }
    }
    return this.set('permissions', permissions)
  }

  /**
   * @param {string} value
   * @return {User}
   */
  updateWork(value) {
    return this.set('work', value)
  }

  /**
   * @param {string} value
   * @return {User}
   */
  updateTelephone(value) {
    return this.set('telephone', value)
  }

  /**
   * @param {string} value
   * @return {User}
   */
  updateMailAddress(value) {
    return this.set('mailAddress', value)
  }

  /**
   * @return {bool}
   */
  isReadytoCreate() {
    if (this.account.length === 0) {
      return false
    }
    return true
  }
}
