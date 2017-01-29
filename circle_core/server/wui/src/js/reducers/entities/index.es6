import {handleActions} from 'redux-actions'
import {Map} from 'immutable'

import schemasActionsHandler from './schemas'
import modulesActionsHandler from './modules'
import usersActionsHandler from './users'
import invitationsActionsHandler from './invitations'


const initialState = {
  invitations: new Map(),
  modules: new Map(),
  // 自分のUserオブジェクトのuuid
  myID: null,
  schemas: new Map(),
  schemaPropertyTypes: new Map(),
  users: new Map(),
}


const entities = handleActions({
  ...schemasActionsHandler,
  ...modulesActionsHandler,
  ...usersActionsHandler,
  ...invitationsActionsHandler,
}, initialState)

export default entities
