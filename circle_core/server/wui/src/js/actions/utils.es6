import {createAction} from 'redux-actions'


export const nullPayloadCreator = () => null


const toUpperSnakeCase = (str) => str.replace(/[A-Z]/g, (s) => '_' + s).toUpperCase()

const createActionType = (prefix, type) => `@@circleCore/${toUpperSnakeCase(prefix)}_${toUpperSnakeCase(type)}`

export const createCcActions = (prefix, payloadCreators) => {
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
