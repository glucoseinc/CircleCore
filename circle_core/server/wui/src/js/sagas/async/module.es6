import CCAPI from '../../api'
import actions, {actionTypes} from '../../actions'
import Module from '../../models/Module'

import {createAsyncSagaParam} from './utils'


// Create
const moduleCreateParam = createAsyncSagaParam(
    ::CCAPI.postModule,
    (payload) => Module.fromObject(payload),
    actions.modules.createSucceeded,
    actions.modules.createFailed,
)

// Read
const moduleFetchParam = createAsyncSagaParam(
  ::CCAPI.getModule,
  (payload) => payload,
  actions.module.fetchSucceeded,
  actions.module.fetchFailed
)

// Read all
const allModulesFetchParam = createAsyncSagaParam(
  ::CCAPI.getModules,
  () => null,
  actions.modules.fetchSucceeded,
  actions.modules.fetchFailed
)

// Update
const moduleUpdateParam = createAsyncSagaParam(
  ::CCAPI.putModule,
  (payload) => Module.fromObject(payload),
  actions.modules.updateSucceeded,
  actions.modules.updateFailed,
)

// Delete
const moduleDeleteParam = createAsyncSagaParam(
  ::CCAPI.deleteModule,
  (payload) => Module.fromObject(payload),
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
