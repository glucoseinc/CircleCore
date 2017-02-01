import {Map} from 'immutable'
import {normalize} from 'normalizr'

import Module from 'src/models/Module'
import Schema from 'src/models/Schema'
import SchemaPropertyType from 'src/models/SchemaPropertyType'
import normalizerSchema from 'src/models/normalizerSchema'


export const convertValues = (obj, converter) => {
  if (typeof obj === 'undefined') {
    return {}
  }
  return Object.entries(obj).reduce((_obj, [key, value]) => ({
    ..._obj,
    [key]: converter(value),
  }), {})
}

export const getNewEntities = (response) => {
  const normalized = normalize(response, normalizerSchema)
  const entities = normalized.entities
  return {
    schemas: new Map(convertValues(entities.schemas, Schema.fromObject)),
    schemaPropertyTypes: new Map(convertValues(entities.schemaPropertyTypes, SchemaPropertyType.fromObject)),
    modules: new Map(convertValues(entities.modules, Module.fromObject)),
  }
}