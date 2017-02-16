/* eslint-disable new-cap */
import {Record} from 'immutable'
import moment from 'moment'


const CcInfoRecord = Record({
  uuid: '',
  displayName: '',
  myself: false,
  work: '',
  lastAccessedAt: null,
})

/**
 * CircleCoreInfo
 */
export default class CcInfo extends CcInfoRecord {
  /**
   * @override
   */
  constructor(...args) {
    super(...args)
    this.label = this.displayName || this.uuid
  }

  /**
   * @param {object} rawCcInfo
   * @return {ReplicationLink}
   */
  static fromObject(rawCcInfo) {
    return new CcInfo({
      uuid: rawCcInfo.uuid || '',
      displayName: rawCcInfo.displayName || '',
      myself: rawCcInfo.myself || false,
      work: rawCcInfo.work || '',
      lastAccessedAt: rawCcInfo.lastAccessedAt ? moment(rawCcInfo.lastAccessedAt) : null,
    })
  }

  /**
   * CcInfoが接続済か示す
   * @return {bool}
   */
  isSynced() {
    return this.lastAccessedAt ? true : false
  }

  /**
   * @param {string} value
   * @return {Schema}
   */
  updateDisplayName(value) {
    return this.set('displayName', value)
  }

  /**
   * @param {string} value
   * @return {Schema}
   */
  updateWork(value) {
    return this.set('work', value)
  }

  /**
   * @return {bool}
   */
  isReadyToCreate() {
    return true
  }
}
