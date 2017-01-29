import {actionTypes} from 'src/actions'

import {getNewEntities} from './utils'


const mergeByFetchingModules = (refresh) => (state, action) => {
  const newEntities = getNewEntities(action.payload)
  return {
    ...state,
    schemas: state.schemas.merge(newEntities.schemas),
    modules: refresh ? newEntities.modules : state.modules.merge(newEntities.modules),
  }
}

const modulesActionsHandler = {
  [actionTypes.modules.fetchSucceeded]: mergeByFetchingModules(true),
  [actionTypes.module.fetchSucceeded]: mergeByFetchingModules(false),
}

export default modulesActionsHandler
