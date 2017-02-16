import CCAPI from 'src/api'
import actions, {actionTypes} from 'src/actions'

import {createAsyncSagaParam} from './utils'


// Fetch all
const allSchemaPropertyTypesFetchParam = createAsyncSagaParam(
  ::CCAPI.fetchAllSchemaPropertyTypes,
  () => null,
  actions.schemaPropertyType.fetchAllSucceeded,
  actions.schemaPropertyType.fetchAllFailed
)


const asyncSagaParams = {
  // Fetch all
  [actionTypes.schemaPropertyType.fetchAllRequest]: allSchemaPropertyTypesFetchParam,
}

export default asyncSagaParams
