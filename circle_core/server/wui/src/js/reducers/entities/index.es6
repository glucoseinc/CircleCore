import {handleActions} from 'redux-actions'
import {Map} from 'immutable'

import ccInfosActionsHandler from './ccInfos'
import invitationsActionsHandler from './invitations'
import modulesActionsHandler from './modules'
import replicationLinksActionsHandler from './replicationLinks'
import schemasActionsHandler from './schemas'
import usersActionsHandler from './users'

const initialState = {
  ccInfos: new Map(),
  invitations: new Map(),
  modules: new Map(),
  myID: null,  // 自分のUserオブジェクトのuuid
  replicationLinks: new Map(),
  schemas: new Map(),
  schemaPropertyTypes: new Map(),
  users: new Map(),
}


const entities = handleActions({
  ...ccInfosActionsHandler,
  ...invitationsActionsHandler,
  ...modulesActionsHandler,
  ...replicationLinksActionsHandler,
  ...schemasActionsHandler,
  ...usersActionsHandler,
}, initialState)

export default entities
