import {Map} from 'immutable'
import {normalize} from 'normalizr'

import {actionTypes} from 'src/actions'
import Invitation from 'src/models/Invitation'
import normalizerSchema from 'src/models/normalizerSchema'

import {convertValues} from './utils'


const invitationsActionsHandler = {
  [actionTypes.invitations.fetchComplete]: (state, {payload: {response, error}}) => {
    if(response) {
      const {entities} = normalize(response, normalizerSchema)
      const invitations = new Map(convertValues(entities.invitations, Invitation.fromObject))

      return {...state, invitations}
    }
    return state
  },

  [actionTypes.invitations.createComplete]: (state, {payload: {response, error}}) => {
    if(response) {
      const {entities} = normalize(response, normalizerSchema)
      const invitations = state.invitations.merge(
        new Map(convertValues(entities.invitations, Invitation.fromObject))
      )
      return {...state, invitations}
    }
    return state
  },

  [actionTypes.invitations.deleteComplete]: (state, {payload: {response, error}}) => {
    if(response) {
      const {entities} = normalize(response, normalizerSchema)
      let invitations = state.invitations
      Object.entries(entities.invitations).forEach(([uuid, obj]) => {
        invitations = invitations.delete(uuid)
      })
      return {...state, invitations}
    }
    return state
  },
}

export default invitationsActionsHandler
