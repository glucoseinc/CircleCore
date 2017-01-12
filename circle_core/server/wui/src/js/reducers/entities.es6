import {handleActions} from 'redux-actions'
import {Map} from 'immutable'
import {normalize} from 'normalizr'

import actionTypes from '../actions/actionTypes'
import Module from '../models/Module'
import Schema from '../models/Schema'
import SchemaPropertyType from '../models/SchemaPropertyType'
import User from '../models/User'
import normalizerSchema from '../models/normalizerSchema'


const initialState = {
  schemas: new Map(),
  schemaPropertyTypes: new Map(),
  modules: new Map(),
  users: [],
}

const convertValues = (obj, converter) => {
  if (typeof obj === 'undefined') {
    return {}
  }
  return Object.entries(obj).reduce((_obj, [key, value]) => ({
    ..._obj,
    [key]: converter(value),
  }), {})
}

const getNewEntities = (response) => {
  const normalized = normalize(response, normalizerSchema)
  const entities = normalized.entities
  return {
    schemas: new Map(convertValues(entities.schemas, Schema.fromObject)),
    schemaPropertyTypes: new Map(convertValues(entities.schemaPropertyTypes, SchemaPropertyType.fromObject)),
    modules: new Map(convertValues(entities.modules, Module.fromObject)),
  }
}

const mergeByFetchingSchemas = (refresh) => (state, action) => {
  const newEntities = getNewEntities(action.payload)
  return {
    ...state,
    schemas: refresh ? newEntities.schemas : state.schemas.merge(newEntities.schemas),
    modules: newEntities.modules.merge(state.modules), // newModules are imperfect
  }
}

const mergeByFetchingModules = (refresh) => (state, action) => {
  const newEntities = getNewEntities(action.payload)
  return {
    ...state,
    schemas: state.schemas.merge(newEntities.schemas),
    modules: refresh ? newEntities.modules : state.modules.merge(newEntities.modules),
  }
}

const setSchemaPropertyTypes = () => (state, action) => {
  const newEntities = getNewEntities(action.payload)
  return {
    ...state,
    schemaPropertyTypes: newEntities.schemaPropertyTypes, // do not merge
  }
}

const entities = handleActions({
  // Fetched Schemas
  [actionTypes.schemas.fetchSucceeded]: mergeByFetchingSchemas(true),
  [actionTypes.schema.fetchSucceeded]: mergeByFetchingSchemas(false),

  // Fetched Schema property types
  [actionTypes.schemaPropertyTypes.fetchSucceeded]: setSchemaPropertyTypes(),

  // Fetched Modules
  [actionTypes.modules.fetchSucceeded]: mergeByFetchingModules(true),
  [actionTypes.module.fetchSucceeded]: mergeByFetchingModules(false),

  // Fetched Users
  [actionTypes.users.fetchSucceeded]: (state, action) => {
    const rawUsers = action.payload
    return {
      ...state,
      users: rawUsers.map(User.fromObject),
    }
  },
}, initialState)

export default entities
