/* eslint-disable new-cap */
import {Record} from 'immutable'


const SchemaPropertyTypeRecord = Record({
  name: '',
})

/**
 */
export default class SchemaPropertyType extends SchemaPropertyTypeRecord {
  /**
   * @param {object} rawSchemaPropertyType
   * @return {SchemaPropertyType}
   */
  static fromObject(rawSchemaPropertyType) {
    return new SchemaPropertyType({
      name: rawSchemaPropertyType.name ? rawSchemaPropertyType.name.toUpperCase() : '',
    })
  }
}
