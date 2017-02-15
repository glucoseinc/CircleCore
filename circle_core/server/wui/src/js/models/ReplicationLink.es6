/* eslint-disable new-cap */
import {Record, List} from 'immutable'


const ReplicationLinkRecord = Record({
  uuid: '',
  displayName: '',
  link: '',
  slaves: List(),
  messageBoxes: List(),
  memo: '',
})

/**
 * ReplicationLink
 */
export default class ReplicationLink extends ReplicationLinkRecord {
  /**
   * @override
   */
  constructor(...args) {
    super(...args)
    this.label = this.displayName || this.uuid
  }

  /**
   * @param {object} rawReplicationLink
   * @return {ReplicationLink}
   */
  static fromObject(rawReplicationLink) {
    return new ReplicationLink({
      uuid: rawReplicationLink.uuid || '',
      displayName: rawReplicationLink.displayName || '',
      link: rawReplicationLink.link || '',
      slaves: List(rawReplicationLink.slaves || []),
      messageBoxes: List(rawReplicationLink.messageBoxes || []),
      memo: rawReplicationLink.memo || '',
    })
  }

  /**
   * get Replication endpoint
   * @return {str} url
   */
  get url() {
    return this.link
  }

  /**
   * @param {string} value
   * @return {ReplicationLink}
   */
  updateDisplayName(value) {
    return this.set('displayName', value)
  }

  /**
   * @param {string} value
   * @return {ReplicationLink}
   */
  addMessageBox(value) {
    if (this.messageBoxes.includes(value)) {
      return this
    }
    const newMessageBox = this.messageBoxes.push(value)
    return this.set('messageBoxes', newMessageBox)
  }

  /**
   * @param {string} value
   * @return {ReplicationLink}
   */
  deleteMessageBox(value) {
    const newMessageBox = this.messageBoxes.filter((messageBox) => messageBox !== value)
    return this.set('messageBoxes', newMessageBox)
  }

  /**
   * @param {array} valueList
   * @return {ReplicationLink}
   */
  updateMessageBoxes(valueList) {
    return this.set('messageBoxes', new List(valueList))
  }

  /**
   * @return {ReplicationLink}
   */
  clearMessageBoxes() {
    return this.set('messageBoxes', new List())
  }

  /**
   * @param {string} value
   * @return {ReplicationLink}
   */
  updateMemo(value) {
    return this.set('memo', value)
  }

  /**
   * @return {bool}
   */
  isReadyToCreate() {
    if (this.messageBoxes.size === 0) {
      return false
    }
    if (this.displayName.length === 0) {
      return false
    }
    return true
  }
}
