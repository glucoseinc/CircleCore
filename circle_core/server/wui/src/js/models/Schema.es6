/* eslint-disable new-cap */
import {Record, List} from 'immutable'


const SchemaPropertyRecord = Record({
  name: '',
  type: '',
})

/**
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

  /**
   * @return {string}
   */
  toString() {
    return `${this.name}:${this.type}`
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
   * @param {number} index
   * @param {object} value
   * @return {Schema}
   */
  updateSchemaPropertyName(index, value) {
    const newProperties = this.properties.update(index, (property) => property.set('name', value))
    return this.set('properties', newProperties)
  }

  /**
   * @param {number} index
   * @param {object} value
   * @return {Schema}
   */
  updateSchemaPropertyType(index, value) {
    const newProperties = this.properties.update(index, (property) => property.set('type', value))
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
    return true
  }

  /**
   * @return {string}
   */
  propertiesToString() {
    return this.properties.map((property) => property.toString()).join(', ')
  }
}
