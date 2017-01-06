import {createCcActions, nullPayloadCreator} from './utils'


const payloadCreators = {
  update: (schema) => schema.toJS(),
  createInit: nullPayloadCreator,
}

const ccActions = createCcActions('schema', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
