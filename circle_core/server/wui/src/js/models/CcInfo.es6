/* eslint-disable new-cap */
import {Record} from 'immutable'


const CcInfoRecord = Record({
  uuid: '',
  displayName: '',
  myself: false,
  work: '',
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
    })
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
  updateWord(value) {
    return this.set('work', value)
  }

  /**
   * @return {bool}
   */
  isReadytoCreate() {
    return true
  }
}