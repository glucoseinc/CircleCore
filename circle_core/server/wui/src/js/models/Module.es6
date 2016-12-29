/* eslint-disable new-cap */
import {Record, List} from 'immutable'

import MessageBox from '../models/MessageBox'


const ModuleRecord = Record({
  uuid: '',
  messageBoxes: List(),
  display_name: '',
  tags: List(),
  description: '',
})

/**
 */
export default class Module extends ModuleRecord {
  /**
   * @param {object} rawModule
   * @return {Module}
   */
  static fromObject(rawModule) {
    const messageBoxes = rawModule.messageBoxes ? rawModule.messageBoxes.map(MessageBox.fromObject) : null
    return new Module({
      uuid: rawModule.uuid || '',
      messageBoxes: List(messageBoxes),
      display_name: rawModule.display_name || '',
      tags: List(rawModule.tags),
      description: rawModule.description || '',
    })
  }
}
