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

// Fetch token
const userFetchTokenParam = createAsyncSagaParam(
  ::CCAPI.fetchUserToken,
  (payload) => payload,
  actions.user.fetchTokenSucceeded,
  actions.user.fetchTokenFailed
)

// Update
const userUpdateParam = createAsyncSagaParam(
  ::CCAPI.updateUser,
  (payload) => payload,
  actions.user.updateSucceeded,
  actions.user.updateFailed,
)

// Generate token
const userGenerateTokenParam = createAsyncSagaParam(
  ::CCAPI.generateUserToken,
  (payload) => payload,
  actions.user.generateTokenSucceeded,
  actions.user.generateTokenFailed,
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

  // Fetch token
  [actionTypes.user.fetchTokenRequest]: userFetchTokenParam,

  // Update
  [actionTypes.user.updateRequest]: userUpdateParam,

  // Generate token
  [actionTypes.user.generateTokenRequest]: userGenerateTokenParam,

  // Delete
  [actionTypes.user.deleteRequest]: userDeleteParam,
}

export default asyncSagaParams
