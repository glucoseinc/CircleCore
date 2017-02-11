import {handleActions} from 'redux-actions'
import {Map} from 'immutable'

import ccInfosActionsHandler from './ccInfos'
import invitationsActionsHandler from './invitations'
import modulesActionsHandler from './modules'
import replicationLinksActionsHandler from './replicationLinks'
import schemaActionsHandler from './schema'
import userActionsHandler from './user'

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
  ...schemaActionsHandler,
  ...userActionsHandler,
}, initialState)

export default entities
