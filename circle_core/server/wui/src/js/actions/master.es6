import actionTypes from '../constants/ActionTypes'

/**
 * [leftIconButtonTouchTap description]
 * @return {[type]} [description]
 */
export function leftIconButtonTouchTap() {
  return {type: actionTypes.navDrawer.toggleOpen}
}

/**
 * [navDrawerRequestChange description]
 * @return {[type]} [description]
 */
export function navDrawerRequestChange() {
  return {type: actionTypes.navDrawer.toggleOpen}
}

/**
 * [locationRequestChange description]
 * @param  {[type]} pathname [description]
 * @return {[type]}          [description]
 */
export function locationRequestChange(pathname) {
  return {type: actionTypes.location.changeRequested, pathname: pathname}
}
