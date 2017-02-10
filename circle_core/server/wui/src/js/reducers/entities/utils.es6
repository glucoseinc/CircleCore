import {Map} from 'immutable'
import {normalize} from 'normalizr'

import CcInfo from 'src/models/CcInfo'
import Module from 'src/models/Module'
import ReplicationLink from 'src/models/ReplicationLink'
import Schema from 'src/models/Schema'
import SchemaPropertyType from 'src/models/SchemaPropertyType'
import User from 'src/models/User'
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
    ccInfos: new Map(convertValues(entities.ccInfos, CcInfo.fromObject)),
    modules: new Map(convertValues(entities.modules, Module.fromObject)),
    replicationLinks: new Map(convertValues(entities.replicationLinks, ReplicationLink.fromObject)),
    schemas: new Map(convertValues(entities.schemas, Schema.fromObject)),
    schemaPropertyTypes: new Map(convertValues(entities.schemaPropertyTypes, SchemaPropertyType.fromObject)),
    users: new Map(convertValues(entities.users, User.fromObject)),
  }
}
