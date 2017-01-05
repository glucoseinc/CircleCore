import React from 'react'
import {render} from 'react-dom'
import {Provider} from 'react-redux'
import {Router, browserHistory} from 'react-router'
import {syncHistoryWithStore} from 'react-router-redux'
import injectTapEventPlugin from 'react-tap-event-plugin'

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'

import configureStore from './store/configureStore'
import rootSaga from './sagas'
import rootRoute from './routes'

injectTapEventPlugin()

const initialState = {}
const store = configureStore(browserHistory, initialState)
store.runSaga(rootSaga)
const history = syncHistoryWithStore(browserHistory, store)

render(
  <Provider store={store}>
    <MuiThemeProvider muiTheme={getMuiTheme()}>
      <Router history={history} routes={rootRoute} />
    </MuiThemeProvider>
  </Provider>,
  document.getElementById('app')
)
