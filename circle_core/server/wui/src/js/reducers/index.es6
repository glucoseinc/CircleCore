import {combineReducers} from 'redux'
import {routerReducer as routing} from 'react-router-redux'

import entities from './entities'
import asyncs from './asyncs'
import miscs from './miscs'

const rootReducer = combineReducers({
  entities,
  asyncs,
  miscs,
  routing,
})

export default rootReducer
