import {fork} from 'redux-saga/effects'

import schemasSaga from './schemas'
import modulesSaga from './modules'
import loationSage from './location'

/**
 * [rootSaga description]
 */
export default function* rootSaga() {
  yield fork(schemasSaga)
  yield fork(modulesSaga)
  yield fork(loationSage)
}
