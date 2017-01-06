import {createCcActions} from './utils'


const payloadCreators = {
  navDrawerToggleOpen: (value) => value,
  inputTextChange: (inputText) => inputText,
}

const ccActions = createCcActions('misc', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
