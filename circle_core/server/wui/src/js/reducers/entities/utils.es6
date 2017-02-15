import {Map} from 'immutable'
import {normalize} from 'normalizr'

import CcInfo from 'src/models/CcInfo'
import Invitation from 'src/models/Invitation'
import Module from 'src/models/Module'
import ReplicationLink from 'src/models/ReplicationLink'
import Schema from 'src/models/Schema'
import SchemaPropertyType from 'src/models/SchemaPropertyType'
import User from 'src/models/User'
import normalizerSchema from 'src/models/normalizerSchema'


export const convertValues = (obj, converter, ...args) => {
  if (typeof obj === 'undefined') {
    return {}
  }
  return Object.entries(obj).reduce((_obj, [key, value]) => ({
    ..._obj,
    [key]: converter(value, ...args),
  }), {})
}

export const getNewEntities = (response) => {
  const normalized = normalize(response, normalizerSchema)
  const entities = normalized.entities

  const messageBoxes = new Map(convertValues(entities.messageBoxes, MessageBox.fromObject))

  return {
    ccInfos: new Map(convertValues(entities.ccInfos, CcInfo.fromObject)),
    invitations: new Map(convertValues(entities.invitations, Invitation.fromObject)),
    modules: new Map(convertValues(entities.modules, Module.fromObject)),
    replicationLinks: new Map(convertValues(entities.replicationLinks, ReplicationLink.fromObject)),
    schemas: new Map(convertValues(entities.schemas, Schema.fromObject)),
    schemaPropertyTypes: new Map(convertValues(entities.schemaPropertyTypes, SchemaPropertyType.fromObject)),
    users: new Map(convertValues(entities.users, User.fromObject)),
  }
}
