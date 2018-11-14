import {actionTypes} from 'src/actions'

import {getNewEntities} from './utils'


const mergeUsers = (state, action) => {
  const {
    users,
  } = getNewEntities(action.payload)
  return {
    ...state,
    myID: action.type === actionTypes.user.fetchMyselfSucceeded ? users.keySeq().first() : state.myID,
    users: state.users.merge(users),
  }
}

const refreshUsers = (state, action) => {
  const {
    users,
  } = getNewEntities(action.payload)
  return {
    ...state,
    users,
  }
}

const deleteUsers = (state, action) => {
  const {
    users,
  } = getNewEntities(action.payload)
  return {
    ...state,
    users: state.users.filterNot((user, userId) => users.keySeq().includes(userId)),
  }
}

const userActionsHandler = {
  // Create
  [actionTypes.user.createSucceeded]: mergeUsers,

  // Fetch
  [actionTypes.user.fetchSucceeded]: mergeUsers,

  // Fetch all
  [actionTypes.user.fetchAllSucceeded]: refreshUsers,

  // Fetch myself
  [actionTypes.user.fetchMyselfSucceeded]: mergeUsers,

  // Update
  [actionTypes.user.updateSucceeded]: mergeUsers,

  // Delete
  [actionTypes.user.deleteSucceeded]: deleteUsers,
}

export default userActionsHandler
