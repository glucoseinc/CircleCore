/* eslint-disable new-cap */
import {Record} from 'immutable'


const InvitationRecord = Record({
  uuid: '',
  maxInvites: -1,
  currentInvites: -1,
  dateCreated: null,
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
      dateCreated: rawInvitation.dateCreated,
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
  get link() {
    return `${location.origin}/invitation/${this.uuid}`
  }
}
