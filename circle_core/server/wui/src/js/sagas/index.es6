import {fork} from 'redux-saga/effects'

import locationSage from './location'
import modulesSaga from './modules'
import schemaSaga from './schema'
import moduleSaga from './module'
import loationSage from './location'
import miscSage from './misc'
import usersSaga from './users'


/**
 * [rootSaga description]
 */
export default function* rootSaga() {
  yield fork(locationSage)
  yield fork(modulesSaga)
  yield fork(schemaSaga)
  yield fork(moduleSaga)
  yield fork(loationSage)
  yield fork(miscSage)
  yield fork(usersSaga)
}
