import CCAPI from 'src/api'
import actions, {actionTypes} from 'src/actions'

import {createAsyncSagaParam} from './utils'


// Create
const moduleCreateParam = createAsyncSagaParam(
    ::CCAPI.createModule,
    (payload) => payload,
    actions.module.createSucceeded,
    actions.module.createFailed,
)

// Fetch
const moduleFetchParam = createAsyncSagaParam(
  ::CCAPI.fetchModule,
  (payload) => payload,
  actions.module.fetchSucceeded,
  actions.module.fetchFailed
)

// Fetch all
const allModulesFetchParam = createAsyncSagaParam(
  ::CCAPI.fetchAllModules,
  () => null,
  actions.module.fetchAllSucceeded,
  actions.module.fetchAllFailed
)

// Update
const moduleUpdateParam = createAsyncSagaParam(
  ::CCAPI.updateModule,
  (payload) => payload,
  actions.module.updateSucceeded,
  actions.module.updateFailed,
)

// Delete
const moduleDeleteParam = createAsyncSagaParam(
  ::CCAPI.deleteModule,
  (payload) => payload,
  actions.module.deleteSucceeded,
  actions.module.deleteFailed,
)


const asyncSagaParams = {
  // Create
  [actionTypes.module.createRequest]: moduleCreateParam,

  // Fetch
  [actionTypes.module.fetchRequest]: moduleFetchParam,

  // Fetch all
  [actionTypes.module.fetchAllRequest]: allModulesFetchParam,

  // Update
  [actionTypes.module.updateRequest]: moduleUpdateParam,

  // Delete
  [actionTypes.module.deleteRequest]: moduleDeleteParam,
}

export default asyncSagaParams
