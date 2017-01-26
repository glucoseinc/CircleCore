import CCAPI from 'src/api'
import actions, {actionTypes} from 'src/actions'

import {createAsyncSagaParam} from './utils'


// Create
const moduleCreateParam = createAsyncSagaParam(
    ::CCAPI.createModule,
    (payload) => payload,
    actions.modules.createSucceeded,
    actions.modules.createFailed,
)

// Read
const moduleFetchParam = createAsyncSagaParam(
  ::CCAPI.fetchModule,
  (payload) => payload,
  actions.module.fetchSucceeded,
  actions.module.fetchFailed
)

// Read all
const allModulesFetchParam = createAsyncSagaParam(
  ::CCAPI.fetchAllModules,
  () => null,
  actions.modules.fetchSucceeded,
  actions.modules.fetchFailed
)

// Update
const moduleUpdateParam = createAsyncSagaParam(
  ::CCAPI.updateModule,
  (payload) => payload,
  actions.modules.updateSucceeded,
  actions.modules.updateFailed,
)

// Delete
const moduleDeleteParam = createAsyncSagaParam(
  ::CCAPI.deleteModule,
  (payload) => payload,
  actions.modules.deleteSucceeded,
  actions.modules.deleteFailed,
)


const asyncSagaParams = {
  // Create
  [actionTypes.modules.createRequest]: moduleCreateParam,

  // Read
  [actionTypes.module.fetchRequest]: moduleFetchParam,

  // Read all
  [actionTypes.modules.fetchRequest]: allModulesFetchParam,
  [actionTypes.modules.createSucceeded]: allModulesFetchParam,
  [actionTypes.modules.updateSucceeded]: allModulesFetchParam,
  [actionTypes.modules.deleteSucceeded]: allModulesFetchParam,

  // Update
  [actionTypes.modules.updateRequest]: moduleUpdateParam,

  // Delete
  [actionTypes.modules.deleteRequest]: moduleDeleteParam,
}

export default asyncSagaParams
