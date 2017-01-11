import actionTypes from '../constants/ActionTypes'

const initialState = {
  isSchemasFetching: false,
  isSchemaPropertyFetching: false,
  isSchemaCreating: false,
  isSchemaDeleteAsking: false,

  isModulesFetching: false,
  isModuleCreating: false,
  isModuleUpdating: false,
  isModuleDeleteAsking: false,
}

/**
 * [asyncs description]
 * @param  {[type]} [state=initialState] [description]
 * @param  {[type]} action               [description]
 * @return {[type]}                      [description]
 */
export default function asyncs(state = initialState, action) {
  switch (action.type) {
  case actionTypes.schemas.fetchRequested:
    return {
      ...state,
      isSchemasFetching: true,
    }
  case actionTypes.schemas.fetchSucceeded:
  case actionTypes.schemas.fetchFailed:
    return {
      ...state,
      isSchemasFetching: false,
    }

  case actionTypes.schema.createRequested:
    return {
      ...state,
      isSchemaCreating: true,
    }
  case actionTypes.schema.createSucceeded:
  case actionTypes.schema.createFailed:
    return {
      ...state,
      isSchemaCreating: false,
    }

  case actionTypes.schema.deleteAsked:
    return {
      ...state,
      isSchemaDeleteAsking: true,
    }
  case actionTypes.schema.deleteRequested:
  case actionTypes.schema.deleteCanceled:
    return {
      ...state,
      isSchemaDeleteAsking: false,
    }

  case actionTypes.schema.propertyTypes.fetchRequested:
    return {
      ...state,
      isSchemaPropertyFetching: true,
    }
  case actionTypes.schema.propertyTypes.fetchSucceeded:
  case actionTypes.schema.propertyTypes.fetchFailed:
    return {
      ...state,
      isSchemaPropertyFetching: false,
    }

  case actionTypes.modules.fetchRequested:
    return {
      ...state,
      isModulesFetching: true,
    }
  case actionTypes.modules.fetchSucceeded:
  case actionTypes.modules.fetchFailed:
    return {
      ...state,
      isModulesFetching: false,
    }

  case actionTypes.module.deleteAsked:
    return {
      ...state,
      isModuleDeleteAsking: true,
    }
  case actionTypes.module.deleteRequested:
  case actionTypes.module.deleteCanceled:
    return {
      ...state,
      isModuleDeleteAsking: false,
    }

  default:
    return state
  }
}
