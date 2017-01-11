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
    const Module = require('../models/Module').default
    const properties = rawSchema.properties ? rawSchema.properties.map(SchemaProperty.fromObject) : []
    const modules = rawSchema.modules ? rawSchema.modules.map(Module.fromObject) : []
    return new Schema({
      uuid: rawSchema.uuid || '',
      displayName: rawSchema.displayName || '',
      properties: List(properties),
      modules: List(modules),
      memo: rawSchema.memo || '',
    })
  }

  /**
   * @param {string} key
   * @param {object} value
   * @return {Schema}
   */
  update(key, value) {
    return this.set(key, value)
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
   * @param {string} key
   * @param {object} value
   * @return {Schema}
   */
  updateSchemaProperty(index, key, value) {
    const newProperties = this.properties.update(index, (property) => property.set(key, value))
    return this.set('properties', newProperties)
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
}
