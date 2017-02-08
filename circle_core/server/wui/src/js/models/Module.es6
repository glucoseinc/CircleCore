/* eslint-disable new-cap */
import {Record, List} from 'immutable'


const MessageBoxRecord = Record({
  uuid: '',
  schema: '',
  displayName: '',
  memo: '',
})

/**
 * MessageBoxモデル
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
      memo: rawMessageBox.memo || '',
    })
  }

  /**
   * Schema更新
   * @param {string} value
   * @return {MessageBox}
   */
  updateSchema(value) {
    return this.set('schema', value)
  }

  /**
   * 表示名更新
   * @param {string} value
   * @return {MessageBox}
   */
  updateDisplayName(value) {
    return this.set('displayName', value)
  }

  /**
   * メモ更新
   * @param {string} value
   * @return {MessageBox}
   */
  updateMemo(value) {
    return this.set('memo', value)
  }

  /**
   * @return {bool}
   */
  isValid() {
    return this.displayName.length !== 0 && this.schema.length !== 0
  }
}


const ModuleRecord = Record({
  uuid: '',
  displayName: '',
  messageBoxes: List(),
  tags: List(),
  memo: '',
})

/**
 * Moduleモデル
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
      memo: rawModule.memo || '',
    })
  }

  /**
   * 表示名更新
   * @param {string} value
   * @return {Module}
   */
  updateDisplayName(value) {
    return this.set('displayName', value)
  }

  /**
   * MessageBox追加
   * @param {MessageBox} meessageBox
   * @return {Module}
   */
  pushMessageBox(meessageBox = new MessageBox()) {
    const newMessageBoxes = this.messageBoxes.push(meessageBox)
    return this.set('messageBoxes', newMessageBoxes)
  }

  /**
   * MessageBox削除
   * @param {number} index
   * @return {Module}
   */
  removeMessageBox(index) {
    const newMessageBoxes = this.messageBoxes.delete(index)
    return this.set('messageBoxes', newMessageBoxes)
  }

  /**
   * MessageBox更新
   * @param {number} index
   * @param {MessageBox} messageBox
   * @return {Module}
   */
  updateMessageBox(index, messageBox) {
    const newMessageBoxes = this.messageBoxes.set(index, messageBox)
    return this.set('messageBoxes', newMessageBoxes)
  }


  /**
   * MessageBoxをまとめて更新
   * @param {List} messageBoxes
   * @return {Module}
   */
  updateMessageBoxes(messageBoxes) {
    return this.set('messageBoxes', messageBoxes)
  }

  /**
   * tag追加
   * @param {string} tag
   * @return {Module}
   */
  pushTag(tag = '') {
    const newTags = this.tags.push(tag)
    return this.set('tags', newTags)
  }

  /**
   * tag削除
   * @param {number} index
   * @return {Module}
   */
  removeTag(index) {
    const newTags = this.tags.delete(index)
    return this.set('tags', newTags)
  }

  /**
   * tag更新
   * @param {number} index
   * @param {string} tag
   * @return {Module}
   */
  updateTag(index, tag) {
    const newTags = this.tags.set(index, tag)
    return this.set('tags', newTags)
  }

  /**
   * メモ更新
   * @param {string} value
   * @return {Schema}
   */
  updateMemo(value) {
    return this.set('memo', value)
  }

  /**
   * 作成可能か
   * @return {bool}
   */
  isReadytoCreate() {
    if (this.messageBoxes.filterNot((messageBox) => messageBox.isValid()).size !== 0) {
      return false
    }
    if (this.tags.filter((tag) => tag === '').size !== 0) {
      return false
    }
    if (this.displayName.length === 0) {
      return false
    }
    return true
  }
}
