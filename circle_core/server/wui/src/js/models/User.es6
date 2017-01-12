/* eslint-disable new-cap */
import {Record} from 'immutable'


const UserRecord = Record({
  uuid: '',
  mailAddress: '',
  permissions: [],
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
      mailAddress: rawUser.mailAddress,
      permissions: rawUser.permissions,
    })
  }

  /**
   * 表示用の名称
   * @return {string}
   */
  get displayName() {
    return this.mailAddress || this.uuid
  }

  /**
   * 管理者であるか？
   * @return {bool}
   */
  get isAdmin() {
    return this.permissions.indexOf('admin') >= 0
  }
}
