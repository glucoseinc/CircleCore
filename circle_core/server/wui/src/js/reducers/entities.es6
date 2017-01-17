import {handleActions} from 'redux-actions'
import {Map} from 'immutable'
import {normalize} from 'normalizr'

import {actionTypes} from '../actions'
import Invitation from '../models/Invitation'
import Module from '../models/Module'
import Schema from '../models/Schema'
import SchemaPropertyType from '../models/SchemaPropertyType'
import User from '../models/User'
import normalizerSchema from '../models/normalizerSchema'


const initialState = {
  invitations: new Map(),
  modules: new Map(),
  schemas: new Map(),
  schemaPropertyTypes: new Map(),
  users: new Map(),
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
  [actionTypes.users.fetchComplete]: (state, {payload: {response, error}}) => {
    if(response) {
      const {entities} = normalize(response, normalizerSchema)
      const users = new Map(convertValues(entities.users, User.fromObject))

      return {...state, users}
    }
    return state
  },

  [actionTypes.users.deleteComplete]: (state, {payload: {response, error}}) => {
    if(response) {
      // 削除されるUserはたかだか1個なのでこの実装で問題ないと思う
      const {entities} = normalize(response, normalizerSchema)
      let users = state.users
      Object.entries(entities.users).forEach(([uuid, obj]) => {
        users = users.delete(uuid)
      })
      return {...state, users}
    }
    return state
  },

  [actionTypes.user.updateComplete]: (state, {payload: {response, error}}) => {
    if(response) {
      const {entities} = normalize(response, normalizerSchema)
      const users = state.users.merge(
        new Map(convertValues(entities.users, User.fromObject))
      )
      return {...state, users}
    }
    return state
  },

  // Fetched Invitations
  [actionTypes.invitations.fetchComplete]: (state, {payload: {response, error}}) => {
    if(response) {
      const {entities} = normalize(response, normalizerSchema)
      const invitations = new Map(convertValues(entities.invitations, Invitation.fromObject))

      return {...state, invitations}
    }
    return state
  },

  [actionTypes.invitations.createComplete]: (state, {payload: {response, error}}) => {
    if(response) {
      const {entities} = normalize(response, normalizerSchema)
      const invitations = state.invitations.merge(
        new Map(convertValues(entities.invitations, Invitation.fromObject))
      )
      return {...state, invitations}
    }
    return state
  },

  [actionTypes.invitations.deleteComplete]: (state, {payload: {response, error}}) => {
    if(response) {
      const {entities} = normalize(response, normalizerSchema)
      let invitations = state.invitations
      Object.entries(entities.invitations).forEach(([uuid, obj]) => {
        invitations = invitations.delete(uuid)
      })
      return {...state, invitations}
    }
    return state
  },
}, initialState)

export default entities
