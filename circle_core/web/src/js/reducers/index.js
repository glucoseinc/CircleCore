import {connectRouter} from 'connected-react-router'
import {combineReducers} from 'redux'

import asyncs from './asyncs'
import auth from './auth'
import entities from './entities'
import error from './error'
import misc from './misc'
import page from './page'


const createRootReducer = (history) => combineReducers({
  router: connectRouter(history),
  asyncs,
  auth,
  entities,
  error,
  misc,
  page,
})

export default createRootReducer
