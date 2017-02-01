import {handleActions} from 'redux-actions'
import {Map} from 'immutable'

import ReplicationLink from 'src/models/ReplicationLink'  // TODO: For Mock

import invitationsActionsHandler from './invitations'
import modulesActionsHandler from './modules'
import schemasActionsHandler from './schemas'
import usersActionsHandler from './users'

const mockReplicationLinks = {
  '11111111-1111-1111-1111-111111111111': ReplicationLink.fromObject({
    uuid: '11111111-1111-1111-1111-111111111111',
    displayName: '共有リンク01',
    message_boxes: ['52ba04f4-84ae-4127-b441-6b37ad293792'],
    memo: '共有リンク01メモ',
  }),
  '22222222-2222-2222-2222-222222222222': ReplicationLink.fromObject({
    uuid: '22222222-2222-2222-2222-222222222222',
    displayName: '共有リンク02',
    label: '共有リンク02',
    message_boxes: ['52ba04f4-84ae-4127-b441-6b37ad293792'],
    memo: '共有リンク02メモ',
  }),
}

const initialState = {
  invitations: new Map(),
  modules: new Map(),
  myID: null,  // 自分のUserオブジェクトのuuid
  replicationLinks: new Map(mockReplicationLinks), // TODO: Remove Mock
  schemas: new Map(),
  schemaPropertyTypes: new Map(),
  users: new Map(),
}


const entities = handleActions({
  ...invitationsActionsHandler,
  ...modulesActionsHandler,
  ...schemasActionsHandler,
  ...usersActionsHandler,
}, initialState)

export default entities
