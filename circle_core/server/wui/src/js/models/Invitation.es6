/* eslint-disable new-cap */
import {Record} from 'immutable'
import moment from 'moment'


const InvitationRecord = Record({
  uuid: '',
  maxInvites: -1,
  currentInvites: -1,
  _createdAt: null,
})

/**
 * Userモデル
 */
export default class Invitation extends InvitationRecord {
  /**
   * @override
   */
  constructor(...args) {
    super(...args)
  }

  /**
   * @param {object} rawInvitation
   * @return {Invitation}
   */
  static fromObject(rawInvitation) {
    return new Invitation({
      uuid: rawInvitation.uuid,
      maxInvites: rawInvitation.maxInvites,
      currentInvites: rawInvitation.currentInvites,
      _createdAt: moment.utc(rawInvitation.dateCreated),
    })
  }

  /**
   * 表示用の名称
   * @return {string}
   */
  get displayName() {
    return this.uuid
  }

  /**
   * ユーザー招待リンクのパス
   */
  get url() {
    return `${location.origin}/invitation/${this.uuid}`
  }

  /**
   * 残招待数を返す
   * @return {string}
   */
  get remainingInvites() {
    return this.maxInvites == 0 ? '∞' : this.maxInvites - this.currentInvites
  }

  /**
   * 作成日時を返す
   * @return {string}
   */
  get createdAt() {
    return this._createdAt.isValid() ? this._createdAt.local().format('YY/MM/DD HH:mm') : ''
  }
}
