/* eslint-disable new-cap */
import {Record} from 'immutable'

export const VALID_URL_REX = /^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$/gm


const ReplicationMasterRecord = Record({
  id: 0,
  endpointUrl: '',
})

/**
 * ReplicationLink
 */
export default class ReplicationMaster extends ReplicationMasterRecord {
  /**
   * @override
   */
  constructor(...args) {
    super(...args)
    this.label = this.endpointUrl || `ReplicationMaster ${this.id}`
  }

  /**
   * @param {object} rawData
   * @return {ReplicationMaster}
   */
  static fromObject(rawData) {
    return new ReplicationMaster({
      id: rawData.id,
      endpointUrl: rawData.endpointUrl,
    })
  }

  /**
   * @param {string} value
   * @return {ReplicationMaster}
   */
  updateEndpointUrl(value) {
    return this.set('endpointUrl', value)
  }

  /**
   * @return {bool}
   */
  isReadyToCreate() {
    if (!this.endpointUrl || !this.endpointUrl.match(VALID_URL_REX)) {
      return false
    }
    return true
  }
}
