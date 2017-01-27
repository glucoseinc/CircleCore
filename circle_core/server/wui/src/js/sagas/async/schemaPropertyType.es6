import CCAPI from '../../api'
import actions, {actionTypes} from '../../actions'

import {createAsyncSagaParam} from './utils'


// Read all
const allSchemaPropertyTypesFetchParam = createAsyncSagaParam(
  ::CCAPI.fetchAllSchemaPropertyTypes,
  () => null,
  actions.schemaPropertyTypes.fetchSucceeded,
  actions.schemaPropertyTypes.fetchFailed
)


const asyncSagaParams = {
  // Read all
  [actionTypes.schemaPropertyTypes.fetchRequest]: allSchemaPropertyTypesFetchParam,
}

export default asyncSagaParams
