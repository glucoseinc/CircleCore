import React from 'react'
import {render} from 'react-dom'
import {Provider} from 'react-redux'
import {Router, browserHistory} from 'react-router'
import {syncHistoryWithStore} from 'react-router-redux'

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'

import configureStore from './store/configureStore'
import rootSaga from './sagas'
import rootRoute from './routes'
import muiTheme from './muiTheme'

const initialState = {}
export const store = configureStore(browserHistory, initialState)
store.runSaga(rootSaga)
const history = syncHistoryWithStore(browserHistory, store)


render(
  <Provider store={store}>
    <MuiThemeProvider muiTheme={muiTheme}>
      <Router history={history} routes={rootRoute} />
    </MuiThemeProvider>
  </Provider>,
  document.getElementById('app')
)
