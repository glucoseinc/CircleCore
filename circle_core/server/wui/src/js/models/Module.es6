/* eslint-disable new-cap */
import {Record, List} from 'immutable'


const MessageBoxRecord = Record({
  uuid: '',
  schema: '',
  displayName: '',
  description: '',
})

/**
 */
export class MessageBox extends MessageBoxRecord {
  /**
   * @override
   */
  constructor(...args) {
    super(...args)
    this.label = this.displayName || this.uuid
  }

  /**
   * @param {object} rawMessageBox
   * @return {MessageBox}
   */
  static fromObject(rawMessageBox) {
    return new MessageBox({
      uuid: rawMessageBox.uuid || '',
      schema: rawMessageBox.schema || '',
      displayName: rawMessageBox.displayName || '',
      description: rawMessageBox.description || '',
    })
  }
}


const ModuleRecord = Record({
  uuid: '',
  displayName: '',
  messageBoxes: List(),
  tags: List(),
  description: '',
})

/**
 */
export default class Module extends ModuleRecord {
  /**
   * @override
   */
  constructor(...args) {
    super(...args)
    this.label = this.displayName || this.uuid
  }

  /**
   * @param {object} rawModule
   * @return {Module}
   */
  static fromObject(rawModule) {
    const messageBoxes = rawModule.messageBoxes ? rawModule.messageBoxes.map(MessageBox.fromObject) : []
    return new Module({
      uuid: rawModule.uuid || '',
      displayName: rawModule.displayName || '',
      messageBoxes: List(messageBoxes),
      tags: List(rawModule.tags || []),
      description: rawModule.description || '',
    })
  }

  /**
   * @param {string} key
   * @param {object} value
   * @return {Module}
   */
  update(key, value) {
    return this.set(key, value)
  }

  /**
   * @param {object} rawMessageBox
   * @return {Module}
   */
  pushMessageBox(rawMessageBox = {}) {
    const newMessageBox = MessageBox.fromObject(rawMessageBox)
    const newMessageBoxes = this.messageBoxes.push(newMessageBox)
    return this.set('messageBoxes', newMessageBoxes)
  }

  /**
   * @param {number} index
   * @return {Module}
   */
  removeMessageBox(index) {
    const newMessageBoxes = this.messageBoxes.delete(index)
    return this.set('messageBoxes', newMessageBoxes)
  }
  /**
   * @param {number} index
   * @param {string} key
   * @param {object} value
   * @return {Module}
   */
  updateMessageBox(index, key, value) {
    const newMessageBoxes = this.messageBoxes.update(index, (messageBox) => messageBox.set(key, value))
    return this.set('messageBoxes', newMessageBoxes)
  }

  /**
   * @param {string} tag
   * @return {Module}
   */
  pushTag(tag = '') {
    const newTags = this.tags.push(tag)
    return this.set('tags', newTags)
  }

  /**
   * @param {number} index
   * @return {Module}
   */
  removeTag(index) {
    const newTags = this.tags.delete(index)
    return this.set('tags', newTags)
  }

  /**
   * @return {bool}
   */
  isReadytoCreate() {
    if (this.messageBoxes.filter((messageBox) => messageBox.schema === '').size !== 0) {
      return false
    }
    return true
  }
}
