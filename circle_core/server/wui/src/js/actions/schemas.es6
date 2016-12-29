import actionTypes from '../constants/ActionTypes'


/**
 * [deleteTouchTap description]
 * @param {[type]} schema [description]
 * @return {[type]} [description]
 */
export function deleteTouchTap(schema) {
  return {type: actionTypes.schema.deleteAsked, schema: schema}
}

/**
 * [deleteExecuteTouchTap description]
 * @param {[type]} schema [description]
 * @return {[type]} [description]
 */
export function deleteExecuteTouchTap(schema) {
  return {type: actionTypes.schema.deleteRequested, schema: schema}
}

/**
 * [deleteCancelTouchTap description]
 * @return {[type]} [description]
 */
export function deleteCancelTouchTap() {
  return {type: actionTypes.schema.deleteCanceled}
}
