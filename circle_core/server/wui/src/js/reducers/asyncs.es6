import {handleActions} from 'redux-actions'

import actionTypes from '../actions/actionTypes'


const initialState = {
  isSchemasCreating: false,
  isSchemasFetching: false,
  isSchemasDeleteAsking: false,

  isSchemaPropertyTypesFetching: false,

  isModulesCreating: false,
  isModulesFetching: false,
  isModulesUpdating: false,
  isModulesDeleteAsking: false,

  isSchemaFetching: false,

  isModuleFetching: false,
}

// Schemas
const setSchemasCreating = (newState) => (state, action) => ({
  ...state,
  isSchemasCreating: newState,
})

const setSchemasFetching = (newState) => (state, action) => ({
  ...state,
  isSchemasFetching: newState,
})

const setSchemasDeleteAsking = (newState) => (state, action) => ({
  ...state,
  isSchemasDeleteAsking: newState,
})

const setSchemaPropertyTypesFetching = (newState) => (state, action) => ({
  ...state,
  isSchemaPropertyTypesFetching: newState,
})

// Modules
const setModulesFetching = (newState) => (state, action) => ({
  ...state,
  isModulesFetching: newState,
})

const setModulesUpdating = (newState) => (state, action) => ({
  ...state,
  isModulesUpdating: newState,
})

const setModulesDeleteAsking = (newState) => (state, action) => ({
  ...state,
  isModulesDeleteAsking: newState,
})

// Schema
const setSchemaFetching = (newState) => (state, action) => ({
  ...state,
  isSchemaFetching: newState,
})

// Module
const setModuleFetching = (newState) => (state, action) => ({
  ...state,
  isModuleFetching: newState,
})


const asyncs = handleActions({
  // Create Schemas
  [actionTypes.schemas.createRequest]: setSchemasCreating(true),
  [actionTypes.schemas.createSucceeded]: setSchemasCreating(false),
  [actionTypes.schemas.createFailed]: setSchemasCreating(false),

  // Fetch Schemas
  [actionTypes.schemas.fetchRequest]: setSchemasFetching(true),
  [actionTypes.schemas.fetchSucceeded]: setSchemasFetching(false),
  [actionTypes.schemas.fetchFailed]: setSchemasFetching(false),

  // Delete Schemas
  [actionTypes.schemas.deleteAsk]: setSchemasDeleteAsking(true),
  [actionTypes.schemas.deleteRequest]: setSchemasDeleteAsking(false),
  [actionTypes.schemas.deleteCancel]: setSchemasDeleteAsking(false),

  // Fetch Schema property types
  [actionTypes.schemaPropertyTypes.fetchRequest]: setSchemaPropertyTypesFetching(true),
  [actionTypes.schemaPropertyTypes.fetchSucceeded]: setSchemaPropertyTypesFetching(false),
  [actionTypes.schemaPropertyTypes.fetchFailed]: setSchemaPropertyTypesFetching(false),

  // Fetch Modules
  [actionTypes.modules.fetchRequest]: setModulesFetching(true),
  [actionTypes.modules.fetchSucceeded]: setModulesFetching(false),
  [actionTypes.modules.fetchFailed]: setModulesFetching(false),

  // Update Modules
  [actionTypes.modules.updateRequest]: setModulesUpdating(true),
  [actionTypes.modules.updateSucceeded]: (setModulesUpdating(false)),
  [actionTypes.modules.updateFailed]: setModulesUpdating(false),

  // Delete Modules
  [actionTypes.modules.deleteAsk]: setModulesDeleteAsking(true),
  [actionTypes.modules.deleteRequest]: setModulesDeleteAsking(false),
  [actionTypes.modules.deleteCancel]: setModulesDeleteAsking(false),

  // Fetch Schema
  [actionTypes.schema.fetchRequest]: setSchemaFetching(true),
  [actionTypes.schema.fetchSucceeded]: setSchemaFetching(false),
  [actionTypes.schema.fetchFailed]: setSchemaFetching(false),

  // Fetch Module
  [actionTypes.module.fetchRequest]: setModuleFetching(true),
  [actionTypes.module.fetchSucceeded]: setModuleFetching(false),
  [actionTypes.module.fetchFailed]: setModuleFetching(false),
}, initialState)

export default asyncs
