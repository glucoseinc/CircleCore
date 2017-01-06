import {createCcActions, nullPayloadCreator} from './utils'


const payloadCreators = {
  fetchRequest: nullPayloadCreator,
  fetchSucceeded: (schemaPropertyTypes) => schemaPropertyTypes.map((schemaPropertyType) => schemaPropertyType.toJS()),
  fetchFailed: (message) => message,
}

const ccActions = createCcActions('schemaPropertyTypes', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
