/* eslint-disable new-cap */
import {Record} from 'immutable'

import Schema from '../models/Schema'


const MessageBoxRecord = Record({
  uuid: '',
  schema: null,
  display_name: '',
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
      display_name: rawMessageBox.display_name || '',
      description: rawMessageBox.description || '',
    })
  }
}
