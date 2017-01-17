import {fork} from 'redux-saga/effects'


const sagaset = [
  'auth',
  'invitations',
  'location',
  'misc',
  'module',
  'modules',
  'schema',
  'schemas',
  'users',
]

/**
 * [rootSaga description]
 */
export default function* rootSaga() {
  for(let sagaFile of sagaset) {
    let saga = require(`./${sagaFile}`).default
    yield fork(saga)
  }
}
