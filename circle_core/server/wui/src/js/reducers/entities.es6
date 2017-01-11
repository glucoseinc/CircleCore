import {handleActions} from 'redux-actions'

import actionTypes from '../actions/actionTypes'
import Schema from '../models/Schema'
import SchemaPropertyType from '../models/SchemaPropertyType'
import Module from '../models/Module'


const initialState = {
  schemas: [],
  schemaPropertyTypes: [],
  MessageBoxes: [],
  modules: [],
}


const entities = handleActions({
  // Fetched Schemas
  [actionTypes.schemas.fetchSucceeded]: (state, action) => {
    const rawSchemas = action.payload
    return {
      ...state,
      schemas: rawSchemas.map(Schema.fromObject),
    }
  },

  // Fetched Schema property types
  [actionTypes.schemaPropertyTypes.fetchSucceeded]: (state, action) => {
    const rawSchemaPropertyTypes = action.payload
    return {
      ...state,
      schemaPropertyTypes: rawSchemaPropertyTypes.map(SchemaPropertyType.fromObject),
    }
  },

  // Fetched Modules
  [actionTypes.modules.fetchSucceeded]: (state, action) => {
    const rawModules = action.payload
    return {
      ...state,
      modules: rawModules.map(Module.fromObject),
    }
  },
}, initialState)

export default entities
