import CCAPI from 'src/api'
import actions, {actionTypes} from 'src/actions'

import {createAsyncSagaParam} from './utils'


// Create
const schemaCreateParam = createAsyncSagaParam(
    ::CCAPI.createSchema,
    (payload) => payload,
    actions.schema.createSucceeded,
    actions.schema.createFailed,
)

// Fetch
const schemaFetchParam = createAsyncSagaParam(
  ::CCAPI.fetchSchema,
  (payload) => payload,
  actions.schema.fetchSucceeded,
  actions.schema.fetchFailed
)

// Fetch all
const allSchemasFetchParam = createAsyncSagaParam(
  ::CCAPI.fetchAllSchemas,
  () => null,
  actions.schema.fetchAllSucceeded,
  actions.schema.fetchAllFailed
)

// Delete
const schemaDeleteParam = createAsyncSagaParam(
  ::CCAPI.deleteSchema,
  (payload) => payload,
  actions.schema.deleteSucceeded,
  actions.schema.deleteFailed,
)


const asyncSagaParams = {
  // Create
  [actionTypes.schema.createRequest]: schemaCreateParam,

  // Fetch
  [actionTypes.schema.fetchRequest]: schemaFetchParam,

  // Fetch all
  [actionTypes.schema.fetchAllRequest]: allSchemasFetchParam,

  // Delete
  [actionTypes.schema.deleteRequest]: schemaDeleteParam,
}

export default asyncSagaParams
