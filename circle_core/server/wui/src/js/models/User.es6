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
  dateLastAccess: null,
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
      dateLastAccess: moment(rawUser.dateLastAccess),
    })
  }

  /**
   * 表示用の名称
   * @return {string}
   */
  get displayName() {
    return this.account || this.uuid
  }

  /**
   * 管理者であるか？
   * @return {bool}
   */
  get isAdmin() {
    return this.permissions.indexOf('admin') >= 0
  }
}
