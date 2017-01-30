import {handleActions} from 'redux-actions'
import {LOCATION_CHANGE} from 'react-router-redux'

import {actionTypes} from '../actions'
import Schema from '../models/Schema'
import Module from '../models/Module'


const initialState = {
  schema: new Schema(),
  module: new Module(),
  inputText: '',
  moduleEditingArea: '',
  errorMessage: null,
}


const initialize = () => (state, action) => ({
  ...initialState,
})


// schema
const setSchema = (schema = new Schema()) => (state, action) => ({
  ...state,
  schema,
})

const updateSchema = () => (state, action) => {
  const rawSchema = action.payload
  return {
    ...state,
    schema: Schema.fromObject(rawSchema),
  }
}


// module
const setModule = (module = new Module()) => (state, action) => ({
  ...state,
  module,
})

const updateModule = () => (state, action) => {
  const rawModule = action.payload
  return {
    ...state,
    module: Module.fromObject(rawModule),
  }
}


// inputText
const updateInputText = () => (state, action) => ({
  ...state,
  inputText: action.payload,
})


// moduleEditingArea
const startModuleEdit = () => (state, action) => {
  const {
    rawModule,
    editingArea,
  } = action.payload
  return {
    ...state,
    module: Module.fromObject(rawModule),
    moduleEditingArea: editingArea,
  }
}

const endModuleEdit = () => (state, action) => {
  return {
    ...state,
    module: new Module(),
    moduleEditingArea: '',
  }
}


const misc = handleActions({
  // Location change
  [LOCATION_CHANGE]: initialize(),

  // Schema
  [actionTypes.schema.update]: updateSchema(),
  [actionTypes.schema.createInit]: setSchema(new Schema().pushSchemaProperty()),
  [actionTypes.schemas.deleteAsk]: updateSchema(),
  [actionTypes.schemas.deleteCancel]: setSchema(),
  [actionTypes.schemas.deleteRequest]: setSchema(),

  // Module
  [actionTypes.module.update]: updateModule(),
  [actionTypes.module.createInit]: setModule(new Module().pushMessageBox()),
  [actionTypes.modules.deleteAsk]: updateModule(),
  [actionTypes.modules.deleteCancel]: setModule(),
  [actionTypes.modules.deleteRequest]: setModule(),

  // User
  [actionTypes.users.deleteComplete]: (state, {payload: {error}}) => {
    if(error)
      return {...state, errorMessage: error.message}
    return state
  },

  // misc
  [actionTypes.misc.inputTextChange]: updateInputText(),

  [actionTypes.misc.startModuleEdit]: startModuleEdit(),
  [actionTypes.misc.cancelModuleEdit]: endModuleEdit(),
  [actionTypes.misc.executeModuleEdit]: endModuleEdit(),

  [actionTypes.misc.clearErrorMessage]: (state, action) => {
    return {
      ...state,
      errorMessage: action.payload,
    }
  },
}, initialState)

export default misc
