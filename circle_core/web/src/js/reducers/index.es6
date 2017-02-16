import {combineReducers} from 'redux'
import {routerReducer as routing} from 'react-router-redux'

import asyncs from './asyncs'
import auth from './auth'
import entities from './entities'
import misc from './misc'
import page from './page'


const rootReducer = combineReducers({
  routing,
  asyncs,
  auth,
  entities,
  misc,
  page,
})

export default rootReducer