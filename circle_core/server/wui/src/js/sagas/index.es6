import {fork} from 'redux-saga/effects'

import schemasSaga from './schemas'
import loationSage from './location'

/**
 * [rootSaga description]
 */
export default function* rootSaga() {
  yield fork(schemasSaga)
  yield fork(loationSage)
}
