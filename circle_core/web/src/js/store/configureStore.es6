import {createStore, compose, applyMiddleware} from 'redux'
import createSagaMiddleware from 'redux-saga'
import {routerMiddleware} from 'react-router-redux'

import rootReducer from 'src/reducers'
import DevTools from 'src/containers/DevTools'


/**
 * [configureStore description]
 * @param  {[type]} history      [description]
 * @param  {[type]} initialState [description]
 * @return {[type]}              [description]
 */
export default function configureStore(history, initialState) {
  const sagaMiddleware = createSagaMiddleware()

  const store = createStore(
    rootReducer,
    initialState,
    compose(
      applyMiddleware(routerMiddleware(history), sagaMiddleware),
      DevTools.instrument()
    )
  )
  store.runSaga = sagaMiddleware.run

  return store
}
