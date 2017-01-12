import {createAction} from 'redux-actions'


/**
 * nullPayloadCreator description
 * @return {null} returns null
 */
export function nullPayloadCreator() {
  return null
}

/**
 * toUpperSnakeCase description
 * @param {string} str string to convert
 * @return {string} returns uppser snake cased string
 */
function toUpperSnakeCase(str) {
  return str.replace(/[A-Z]/g, (s) => '_' + s).toUpperCase()
}

/**
 * createActionType description
 * @param {string} prefix prefix
 * @param {string} type type
 * @return {string} action type string
 */
function createActionType(prefix, type) {
  return `@@circleCore/${toUpperSnakeCase(prefix)}_${toUpperSnakeCase(type)}`
}


/**
 * createCcActions description
 * @param {string} prefix prefix
 * @param {object} payloadCreators payloadCreators
 * @return {object} cc actions
 */
export function createCcActions(prefix, payloadCreators) {
  const actionTypes = Object.entries(payloadCreators).reduce((actionTypes, [type, payloadCreator]) => ({
    ...actionTypes,
    [type]: createActionType(prefix, type),
  }), {})
  return {
    actions: Object.entries(payloadCreators).reduce((_actions, [type, payloadCreator]) => ({
      ..._actions,
      [type]: createAction(actionTypes[type], payloadCreator),
    }), {}),
    actionTypes,
  }
}
