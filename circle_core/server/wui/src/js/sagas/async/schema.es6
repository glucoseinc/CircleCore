import CCAPI from 'src/api'
import actions, {actionTypes} from 'src/actions'

import {createAsyncSagaParam} from './utils'


// Create
const schemaCreateParam = createAsyncSagaParam(
    ::CCAPI.createSchema,
    (payload) => payload,
    actions.schemas.createSucceeded,
    actions.schemas.createFailed,
)

// Read
const schemaFetchParam = createAsyncSagaParam(
  ::CCAPI.fetchSchema,
  (payload) => payload,
  actions.schema.fetchSucceeded,
  actions.schema.fetchFailed
)

// Read all
const allSchemasFetchParam = createAsyncSagaParam(
  ::CCAPI.fetchAllSchemas,
  () => null,
  actions.schemas.fetchSucceeded,
  actions.schemas.fetchFailed
)

// Delete
const schemaDeleteParam = createAsyncSagaParam(
  ::CCAPI.deleteSchema,
  (payload) => payload,
  actions.schemas.deleteSucceeded,
  actions.schemas.deleteFailed,
)


const asyncSagaParams = {
  // Create
  [actionTypes.schemas.createRequest]: schemaCreateParam,

  // Read
  [actionTypes.schema.fetchRequest]: schemaFetchParam,

  // Read all
  [actionTypes.schemas.fetchRequest]: allSchemasFetchParam,
  [actionTypes.schemas.createSucceeded]: allSchemasFetchParam,
  [actionTypes.schemas.deleteSucceeded]: allSchemasFetchParam,

  // Delete
  [actionTypes.schemas.deleteRequest]: schemaDeleteParam,
}

export default asyncSagaParams
