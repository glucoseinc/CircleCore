const initialState = {
  schemas: [],
  schemaPropertyTypes: [],
  MessageBoxes: [],
  modules: [],
}

import actionTypes from '../constants/ActionTypes'

/**
 * [schemas description]
 * @param  {[type]} [state=initialState] [description]
 * @param  {[type]} action               [description]
 * @return {[type]}                      [description]
 */
export default function entities(state = initialState, action) {
  switch (action.type) {
  case actionTypes.schemas.fetchSucceeded:
    return {
      ...state,
      schemas: action.schemas,
    }
  case actionTypes.schema.propertyTypes.fetchSucceeded:
    return {
      ...state,
      schemaPropertyTypes: action.schemaPropertyTypes,
    }

  case actionTypes.modules.fetchSucceeded:
    return {
      ...state,
      modules: action.modules,
    }
  default:
    return state
  }
}
