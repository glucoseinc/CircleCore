import React from 'react'
import {render} from 'react-dom'
import {Provider} from 'react-redux'
import {Router, browserHistory} from 'react-router'
import {syncHistoryWithStore} from 'react-router-redux'
import injectTapEventPlugin from 'react-tap-event-plugin'

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'

import configureStore from './store/configureStore'
import rootSaga from './sagas'
import rootRoute from './routes'
import {checkAuthorization} from './Authorization'
import muiTheme from './muiTheme'

injectTapEventPlugin()

const initialState = {}
const store = configureStore(browserHistory, initialState)
store.runSaga(rootSaga)
const history = syncHistoryWithStore(browserHistory, store)


/**
 * 起動ハンドラ。認証済かチェックして、必要あらば認証を行う
 */
async function checkAndStart() {
  // 認証を確認して、必要あらばそっちに行く
  let canContinue = await checkAuthorization()
  if(!canContinue)
    return

  render(
    <Provider store={store}>
      <MuiThemeProvider muiTheme={muiTheme}>
        <Router history={history} routes={rootRoute} />
      </MuiThemeProvider>
    </Provider>,
    document.getElementById('app')
  )
}
checkAndStart()


export {store}
