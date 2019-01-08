import {routerMiddleware} from 'connected-react-router'
import {createStore, compose, applyMiddleware} from 'redux'
import createSagaMiddleware from 'redux-saga'

import createRootReducer from 'src/reducers'

const composeEnhancers =
  typeof window === 'object' && window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__
    ? window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__({})
    : compose


/**
 * [configureStore description]
 * @param  {[type]} history      [description]
 * @param  {[type]} initialState [description]
 * @return {[type]}              [description]
 */
export default function configureStore(history, initialState) {
  const sagaMiddleware = createSagaMiddleware()

  const store = createStore(
    createRootReducer(history),
    initialState,
    composeEnhancers(
      applyMiddleware(routerMiddleware(history), sagaMiddleware),
    )
  )
  store.runSaga = sagaMiddleware.run

  return store
}
