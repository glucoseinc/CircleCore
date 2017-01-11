import {combineReducers} from 'redux'
import {routerReducer as routing} from 'react-router-redux'

import entities from './entities'
import asyncs from './asyncs'
import misc from './misc'


const rootReducer = combineReducers({
  entities,
  asyncs,
  misc,
  routing,
})

export default rootReducer
