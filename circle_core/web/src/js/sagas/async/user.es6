import CCAPI from 'src/api'
import actions, {actionTypes} from 'src/actions'

import {createAsyncSagaParam} from './utils'


// Create
const userCreateParam = createAsyncSagaParam(
    ::CCAPI.createUser,
    (payload) => payload,
    actions.user.createSucceeded,
    actions.user.createFailed,
)

// Fetch
const userFetchParam = createAsyncSagaParam(
  ::CCAPI.fetchUser,
  (payload) => payload,
  actions.user.fetchSucceeded,
  actions.user.fetchFailed
)

// Fetch all
const allUsersFetchParam = createAsyncSagaParam(
  ::CCAPI.fetchAllUsers,
  () => null,
  actions.user.fetchAllSucceeded,
  actions.user.fetchAllFailed
)

// Fetch myself
const myselfUserFetchParam = createAsyncSagaParam(
  ::CCAPI.fetchMyselfUser,
  () => null,
  actions.user.fetchMyselfSucceeded,
  actions.user.fetchMyselfFailed
)

// Update
const userUpdateParam = createAsyncSagaParam(
  ::CCAPI.updateUser,
  (payload) => payload,
  actions.user.updateSucceeded,
  actions.user.updateFailed,
)

// Delete
const userDeleteParam = createAsyncSagaParam(
  ::CCAPI.deleteUser,
  (payload) => payload,
  actions.user.deleteSucceeded,
  actions.user.deleteFailed,
)


const asyncSagaParams = {
  // Create
  [actionTypes.user.createRequest]: userCreateParam,

  // Fetch
  [actionTypes.user.fetchRequest]: userFetchParam,

  // Fetch all
  [actionTypes.user.fetchAllRequest]: allUsersFetchParam,

  // Fetch myself
  [actionTypes.user.fetchMyselfRequest]: myselfUserFetchParam,

  // Update
  [actionTypes.user.updateRequest]: userUpdateParam,

  // Delete
  [actionTypes.user.deleteRequest]: userDeleteParam,
}

export default asyncSagaParams
