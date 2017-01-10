import {fork} from 'redux-saga/effects'

import schemasSaga from './schemas'
import modulesSaga from './modules'
import schemaSaga from './schema'
import moduleSaga from './module'
import loationSage from './location'
import miscSage from './misc'


/**
 * [rootSaga description]
 */
export default function* rootSaga() {
  yield fork(schemasSaga)
  yield fork(modulesSaga)
  yield fork(schemaSaga)
  yield fork(moduleSaga)
  yield fork(loationSage)
  yield fork(miscSage)
}
