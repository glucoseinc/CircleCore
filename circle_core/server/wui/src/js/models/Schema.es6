/* eslint-disable new-cap */
import {Record, List} from 'immutable'


const SchemaPropertyRecord = Record({
  name: '',
  type: '',
})

/**
 * SchemaPropertyモデル
 */
export class SchemaProperty extends SchemaPropertyRecord {
  /**
   * @param {object} rawSchemaProperty
   * @return {SchemaProperty}
   */
  static fromObject(rawSchemaProperty) {
    return new SchemaProperty({
      name: rawSchemaProperty.name || '',
      type: rawSchemaProperty.type || '',
    })
  }

  /**
   * @param {string} value
   * @return {SchemaProperty}
   */
  updateName(value) {
    return this.set('name', value)
  }

  /**
   * @param {string} value
   * @return {SchemaProperty}
   */
  updateType(value) {
    return this.set('type', value)
  }

  /**
   * @return {bool}
   */
  isFill() {
    return this.name.length !== 0 && this.type.length !== 0
  }

  /**
   * @return {bool}
   */
  isValid() {
    return this.isFill() || (this.name.length === 0 && this.type.length === 0)
  }
}


const SchemaRecord = Record({
  uuid: '',
  displayName: '',
  properties: List(),
  modules: List(),
  memo: '',
})

/**
 * Schemaモデル
 */
export default class Schema extends SchemaRecord {
  /**
   * @override
   */
  constructor(...args) {
    super(...args)
    this.label = this.displayName || this.uuid
  }

  /**
   * @param {object} rawSchema
   * @return {Schema}
   */
  static fromObject(rawSchema) {
    const properties = rawSchema.properties ? rawSchema.properties.map(SchemaProperty.fromObject) : []
    return new Schema({
      uuid: rawSchema.uuid || '',
      displayName: rawSchema.displayName || '',
      properties: List(properties),
      modules: List(rawSchema.modules || []),
      memo: rawSchema.memo || '',
    })
  }

  /**
   * @param {string} value
   * @return {Schema}
   */
  updateUuid(value) {
    return this.set('uuid', value)
  }

  /**
   * @param {string} value
   * @return {Schema}
   */
  updateDisplayName(value) {
    return this.set('displayName', value)
  }

  /**
   * @return {Schema}
   */
  pushSchemaProperty() {
    const newProperties = this.properties.push(new SchemaProperty())
    return this.set('properties', newProperties)
  }

  /**
   * @param {number} index
   * @return {Schema}
   */
  removeSchemaProperty(index) {
    const newProperties = this.properties.delete(index)
    return this.set('properties', newProperties)
  }

  /**
   * SchemaProperty更新
   * @param {number} index
   * @param {SchemaProperty} property
   * @return {Schema}
   */
  updateSchemaProperty(index, property) {
    const newProperties = this.properties.set(index, property)
    return this.set('properties', newProperties)
  }

  /**
   * @param {string} value
   * @return {Schema}
   */
  updateMemo(value) {
    return this.set('memo', value)
  }

  /**
   * @return {bool}
   */
  isReadytoCreate() {
    if (this.properties.filter((property) => property.isFill()).size === 0) {
      return false
    }
    if (this.properties.filterNot((property) => property.isValid()).size !== 0) {
      return false
    }
    if (this.displayName.length === 0) {
      return false
    }
    return true
  }
}
