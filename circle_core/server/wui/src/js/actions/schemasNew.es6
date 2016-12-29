import actionTypes from '../constants/ActionTypes'


/**
 * [updateSchema description]
 * @param  {[type]} schema [description]
 * @return {[type]}        [description]
 */
export function updateSchema(schema) {
  return {type: actionTypes.schema.update, schema: schema}
}

/**
 * [createTouchTap description]
 * @param  {[type]} schema [description]
 * @return {[type]}        [description]
 */
export function createTouchTap(schema) {
  return {type: actionTypes.schema.createRequested, schema: schema}
}
