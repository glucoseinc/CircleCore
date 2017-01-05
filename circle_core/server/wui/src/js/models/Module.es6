/* eslint-disable new-cap */
import {Record, List} from 'immutable'

import MessageBox from '../models/MessageBox'


const ModuleMetadataRecord = Record({
  tags: List(),
  description: '',
})

/**
 */
export class ModuleMetadata extends ModuleMetadataRecord {
  /**
   * @param {object} rawModuleMetadata
   * @return {ModuleMetadata}
   */
  static fromObject(rawModuleMetadata) {
    const tags = rawModuleMetadata.tags || []
    return new ModuleMetadata({
      tags: List(tags),
      description: rawModuleMetadata.description || '',
    })
  }
}

const ModuleRecord = Record({
  uuid: '',
  messageBoxes: List(),
  displayName: '',
  metadata: new ModuleMetadata(),
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
      displayName: rawModule.displayName || '',
      metadata: ModuleMetadata.fromObject(rawModule.metadata || {}),
    })
  }
}
