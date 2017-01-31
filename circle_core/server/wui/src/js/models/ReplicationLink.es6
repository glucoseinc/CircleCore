/* eslint-disable new-cap */
import {Record, List} from 'immutable'


const ReplicationLinkRecord = Record({
  uuid: '',
  displayName: '',
  message_boxes: List(),
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
      message_boxes: List(rawReplicationLink.message_boxes || []),
      memo: rawReplicationLink.memo || '',
    })
  }
}
