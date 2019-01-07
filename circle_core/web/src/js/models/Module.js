/* eslint-disable new-cap */
import {Record, List} from 'immutable'


const MessageBoxRecord = Record({
  uuid: '',
  slaveCcInfos: List(),
  schema: '',
  displayName: '',
  memo: '',
  module: '',
  url: '',
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
    require('assert')(typeof rawMessageBox === 'object')
    return new MessageBox({
      uuid: rawMessageBox.uuid || '',
      schema: rawMessageBox.schema || '',
      slaveCcInfos: List(rawMessageBox.slaveCcInfos || []),
      displayName: rawMessageBox.displayName || '',
      module: rawMessageBox.module || null,
      memo: rawMessageBox.memo || '',
      url: rawMessageBox.url || '',
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


const ModuleAttributeRecord = Record({
  name: '',
  value: '',
})

/**
 * ModuleAttributeモデル
 */
export class ModuleAttribute extends ModuleAttributeRecord {
  /**
   * @param {object} rawModuleAttribute
   * @return {ModuleAttribute}
   */
  static fromObject(rawModuleAttribute) {
    return new ModuleAttribute({
      name: rawModuleAttribute.name || '',
      value: rawModuleAttribute.value || '',
    })
  }

  /**
   * @param {string} value
   * @return {ModuleAttribute}
   */
  updateName(value) {
    return this.set('name', value)
  }

  /**
   * @param {string} value
   * @return {ModuleAttribute}
   */
  updateValue(value) {
    return this.set('value', value)
  }
}


const ModuleRecord = Record({
  uuid: '',
  ccUuid: '',
  isReplication: undefined,
  displayName: '',
  messageBoxes: List(),
  tags: List(),
  attributes: List(),
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
   * @param {Map<UUID, MessageBox>} messageBoxes
   * @return {Module}
   */
  static fromObject(rawModule, messageBoxes) {
    let boxes = rawModule.messageBoxes || []
    boxes.sort()
    boxes = boxes.map((boxUuid) => messageBoxes.get(boxUuid))
    const attributes = rawModule.attributes ? rawModule.attributes.map(ModuleAttribute.fromObject) : []

    return new Module({
      uuid: rawModule.uuid || '',
      ccUuid: rawModule.ccUuid || '',
      isReplication: rawModule.isReplication || undefined,
      displayName: rawModule.displayName || '',
      messageBoxes: List(boxes),
      tags: List(rawModule.tags || []),
      attributes: List(attributes),
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
   * ModuleAttribute追加
   * @param {ModuleAttribute} attribute
   * @return {Module}
   */
  pushModuleAttribute(attribute = new ModuleAttribute()) {
    const newAttributes = this.attributes.push(attribute)
    return this.set('attributes', newAttributes)
  }

  /**
   * ModuleAttribute削除
   * @param {number} index
   * @return {Module}
   */
  removeModuleAttribute(index) {
    const newAttributes = this.attributes.delete(index)
    return this.set('attributes', newAttributes)
  }

  /**
   * ModuleAttribute更新
   * @param {number} index
   * @param {ModuleAttribute} attribute
   * @return {Schema}
   */
  updateModuleAttribute(index, attribute) {
    const newAttributes = this.attributes.set(index, attribute)
    return this.set('attributes', newAttributes)
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
  isReadyToCreate() {
    if (this.messageBoxes.filterNot((messageBox) => messageBox.isValid()).size !== 0) {
      // 入力が不完全なMessageBoxがある
      return false
    }
    if (this.tags.filter((tag) => tag.length === 0).size !== 0) {
      // 空欄のタグがある
      return false
    }
    if (this.tags.filter((tag) =>
      this.tags.filter((_tag) => _tag === tag).size > 1
    ).size !== 0) {
      // タグの重複がある
      return false
    }
    if (this.displayName.length === 0) {
      // 表示名が空欄
      return false
    }
    return true
  }
}
