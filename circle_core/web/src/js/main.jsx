import {ConnectedRouter as Router} from 'connected-react-router'
import {createBrowserHistory} from 'history'
import React from 'react'
import {render} from 'react-dom'
import {Provider} from 'react-redux'

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'

import configureStore from './store/configureStore'
import rootSaga from './sagas'
import Routes from './routes'
import muiTheme from './muiTheme'

const history = createBrowserHistory()
const initialState = {}
export const store = configureStore(history, initialState)
store.runSaga(rootSaga)


render(
  <Provider store={store}>
    <MuiThemeProvider muiTheme={muiTheme}>
      <Router history={history}>
        <Routes />
      </Router>
    </MuiThemeProvider>
  </Provider>,
  document.getElementById('app')
)
