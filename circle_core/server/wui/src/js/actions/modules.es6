import actionTypes from '../constants/ActionTypes'


/**
 * [messageBoxTouchTap description]
 * @param  {[type]} messageBox [description]
 */
export function messageBoxTouchTap(messageBox) {
  console.log(messageBox)
  throw new Error('not implemented')  // TODO: implement
}

/**
 * [tagTouchTap description]
 * @param  {[type]} tag [description]
 */
export function tagTouchTap(tag) {
  console.log(tag)
  throw new Error('not implemented')  // TODO: implement
}

/**
 * [deleteTouchTap description]
 * @param {[type]} module [description]
 * @return {[type]} [description]
 */
export function deleteTouchTap(module) {
  return {type: actionTypes.module.deleteAsked, module: module}
}

/**
 * [deleteExecuteTouchTap description]
 * @param {[type]} module [description]
 * @return {[type]} [description]
 */
export function deleteExecuteTouchTap(module) {
  return {type: actionTypes.module.deleteRequested, module: module}
}

/**
 * [deleteCancelTouchTap description]
 * @return {[type]} [description]
 */
export function deleteCancelTouchTap() {
  return {type: actionTypes.module.deleteCanceled}
}
