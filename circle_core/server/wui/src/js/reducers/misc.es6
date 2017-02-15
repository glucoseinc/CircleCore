import {handleActions} from 'redux-actions'
import {LOCATION_CHANGE} from 'react-router-redux'

import {actionTypes} from 'src/actions'

import Invitation from 'src/models/Invitation'

const initialState = {
  isInvitationCreatedDialogOpen: false,
  newInvitation: null,
}


const initialize = () => (state, action) => ({
  ...initialState,
})


const misc = handleActions({
  // Location change
  [LOCATION_CHANGE]: initialize(),

  // Invitation Created
  [actionTypes.invitation.createSucceeded]: (state, action) => {
    return {
      ...state,
      isInvitationCreatedDialogOpen: true,
      newInvitation: Invitation.fromObject(action.payload.invitation),
    }
  },
  [actionTypes.invitation.createdDialogClose]: (state, action) => {
    return {
      ...state,
      isInvitationCreatedDialogOpen: false,
      newInvitation: null,
    }
  },

}, initialState)

export default misc
