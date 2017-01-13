import {createCcActions, nullPayloadCreator, passPayloadCreator} from './utils'


const payloadCreators = {
  navDrawerToggleOpen: passPayloadCreator,
  inputTextChange: passPayloadCreator,
  startModuleEdit: ({module, editingArea}) => ({
    rawModule: module.toJS(),
    editingArea,
  }),
  cancelModuleEdit: nullPayloadCreator,
  executeModuleEdit: (module) => module.toJS(),
  clearErrorMessage: nullPayloadCreator,
}

const ccActions = createCcActions('misc', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
