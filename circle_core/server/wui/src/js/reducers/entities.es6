import {handleActions} from 'redux-actions'
import {Map} from 'immutable'
import {normalize} from 'normalizr'

import {actionTypes} from 'src/actions'
import Invitation from 'src/models/Invitation'
import Module from 'src/models/Module'
import Schema from 'src/models/Schema'
import SchemaPropertyType from 'src/models/SchemaPropertyType'
import User from 'src/models/User'
import normalizerSchema from 'src/models/normalizerSchema'


const initialState = {
  invitations: new Map(),
  modules: new Map(),
  // 自分のUserオブジェクトのuuid
  myID: null,
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

  [actionTypes.users.fetchMeComplete]: (state, {payload: {response, error}}) => {
    if(response) {
      const normalized = normalize(response, normalizerSchema)
      const users = state.users.merge(
        new Map(convertValues(normalized.entities.users, User.fromObject))
      )

      return {...state, users, myID: normalized.result.user}
    } else {
      return {...state, myID: null}
    }
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
