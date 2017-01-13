import {handleActions} from 'redux-actions'
import {LOCATION_CHANGE} from 'react-router-redux'

import actionTypes from '../actions/actionTypes'
import Schema from '../models/Schema'
import Module from '../models/Module'


const initialState = {
  schema: new Schema(),
  module: new Module(),
  navDrawerOpen: false,
  inputText: '',
  moduleEditingArea: '',
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


// navDrawer
const setNavDrawerOpen = (newState) => (state, action) => ({
  ...state,
  navDrawerOpen: newState,
})

const toggleNavDrawerOpen = () => (state, action) => ({
  ...state,
  navDrawerOpen: !state.navDrawerOpen,
})


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
  [actionTypes.location.changeCancel]: setNavDrawerOpen(false),

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

  // misc
  [actionTypes.misc.navDrawerToggleOpen]: toggleNavDrawerOpen(),
  [actionTypes.misc.inputTextChange]: updateInputText(),
  [actionTypes.misc.startModuleEdit]: startModuleEdit(),
  [actionTypes.misc.cancelModuleEdit]: endModuleEdit(),
  [actionTypes.misc.executeModuleEdit]: endModuleEdit(),

}, initialState)

export default misc
