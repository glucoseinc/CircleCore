/* eslint-disable new-cap */
import {Record} from 'immutable'

import Schema from '../models/Schema'


const MessageBoxRecord = Record({
  uuid: '',
  schema: null,
  displayName: '',
  description: '',
})

/**
 */
export default class MessageBox extends MessageBoxRecord {
  /**
   * @param {object} rawMessageBox
   * @return {MessageBox}
   */
  static fromObject(rawMessageBox) {
    return new MessageBox({
      uuid: rawMessageBox.uuid || '',
      schema: Schema.fromObject(rawMessageBox.schema),
      displayName: rawMessageBox.displayName || '',
      description: rawMessageBox.description || '',
    })
  }
}
