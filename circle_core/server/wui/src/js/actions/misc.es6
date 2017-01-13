import {createCcActions, nullPayloadCreator} from './utils'


const payloadCreators = {
  navDrawerToggleOpen: (value) => value,
  inputTextChange: (inputText) => inputText,
  startModuleEdit: ({module, editingArea}) => ({
    rawModule: module.toJS(),
    editingArea,
  }),
  cancelModuleEdit: nullPayloadCreator,
  executeModuleEdit: (module) => module.toJS(),
}

const ccActions = createCcActions('misc', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
