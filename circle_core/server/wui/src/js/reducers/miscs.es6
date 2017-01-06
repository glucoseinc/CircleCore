import {List} from 'immutable'

import actionTypes from '../constants/ActionTypes'
import Schema, {SchemaProperty} from '../models/Schema'
import Module from '../models/Module'

const initialState = {
  navDrawerOpen: false,
  schema: new Schema(),
  module: new Module(),
  searchText: '',
}

/**
 * [miscs description]
 * @param  {[type]} [state=initialState] [description]
 * @param  {[type]} action               [description]
 * @return {[type]}                      [description]
 */
export default function miscs(state = initialState, action) {
  switch (action.type) {
  case actionTypes.location.change:
  case actionTypes.location.changeCanceled:
    return {
      ...state,
      navDrawerOpen: false,
    }
  case actionTypes.navDrawer.toggleOpen:
    return {
      ...state,
      navDrawerOpen: !state.navDrawerOpen,
    }

  case actionTypes.schema.update:
    return {
      ...state,
      schema: action.schema,
    }

  case actionTypes.schema.createInit:
    return {
      ...state,
      schema: new Schema({properties: List([new SchemaProperty()])}),  // eslint-disable-line new-cap
    }

  case actionTypes.schema.deleteAsked:
    return {
      ...state,
      schema: action.schema,
    }
  case actionTypes.schema.deleteRequested:
  case actionTypes.schema.deleteCanceled:
    return {
      ...state,
      schema: new Schema(),
    }

  case actionTypes.modules.filterByTag:
    return {
      ...state,
      searchText: action.payload,
    }

  case actionTypes.module.deleteAsked:
    return {
      ...state,
      module: action.payload,
    }
  case actionTypes.module.deleteRequested:
  case actionTypes.module.deleteCanceled:
    return {
      ...state,
      module: new Module(),
    }

  case actionTypes.miscs.searchTextChange:
    return {
      ...state,
      searchText: action.payload,
    }

  default:
    return state
  }
}
