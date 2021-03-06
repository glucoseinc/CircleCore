/* global CRCR_LOGIN_REDIRECT_TO:false CRCR_LOGIN_IS_FAILED:false CRCR_AUTH_FORM_VALUES:false */
/**
 * 認証がないページ用のReact
 *
 * main.es6は冒頭で認証チェックをしているので...
 */
import {ConnectedRouter as Router, connectRouter, routerMiddleware} from 'connected-react-router'
import {createBrowserHistory} from 'history'
import React from 'react'
import {render} from 'react-dom'
import {Provider} from 'react-redux'
import {Route, Switch} from 'react-router-dom'
import Title from '@shnjp/react-title-component'
import {combineReducers, createStore, applyMiddleware, compose} from 'redux'
import createSagaMiddleware from 'redux-saga'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import FlatButton from 'material-ui/FlatButton'
import TextField from 'material-ui/TextField'
import {fork} from 'redux-saga/effects'

import {colorError} from 'src/colors'
import muiTheme from 'src/muiTheme'
import PublicFrame from 'src/public/frame'
import UserInvitation from 'src/public/invitation'


/**
 * ログイン画面
 */
class OAuthLogin extends React.Component {
  /**
   * @constructor
   */
  constructor(...args) {
    super(...args)

    this.state = {
      errors: {},
    }
    this.accountRef = React.createRef()
    this.passwordRef = React.createRef()
  }

  /**
   * Form送信前のエラーチェック
   * @param {Event} e イベントオブジェクト
   */
  onSubmit(e) {
    const errors = {}

    if (!this.accountRef.current.getValue()) {
      errors['account'] = 'アカウント名は必須です'
    }
    if (!this.passwordRef.current.getValue()) {
      errors['password'] = 'パスワードは必須です'
    }

    if (Object.keys(errors).length) {
      // has error
      e.preventDefault()
    }

    this.setState({errors})
  }

  /**
   * @override
   */
  render() {
    const redirectTo = CRCR_LOGIN_REDIRECT_TO
    const isFailed = CRCR_LOGIN_IS_FAILED
    const {errors} = this.state

    return (
      <div className="logoinForm" style={{margin: '0px auto', width: '320px'}}>
        <Title render={(previousTitle) => `Login | ${previousTitle}`} />

        <form action="/oauth/login" method="POST" onSubmit={::this.onSubmit}>
          <input type="hidden" name="redirect" value={redirectTo} />

          {isFailed && (
            <div style={{color: colorError}}>
              認証できませんでした。<br />
              アカウント、パスワードを確認してください。
            </div>
          )}

          <TextField
            ref={this.accountRef}
            name="account"
            hintText="アカウント"
            floatingLabelText="アカウント"
            errorText={errors.account}
            style={{width: '100%'}}
            autoComplete="username"
          /><br />

          <TextField
            ref={this.passwordRef}
            name="password"
            hintText="パスワード"
            floatingLabelText="パスワード"
            type="password"
            errorText={errors.password}
            style={{width: '100%'}}
            autoComplete="current-password"
          /><br />

          <div className="loginForm-actions" style={{textAlign: 'center'}}>
            <FlatButton label="ログイン" primary={true} type="submit" />
          </div>
        </form>
      </div>
    )
  }
}


/**
 * OAuth認証画面。 UIすっとばして強制的にPOSTしてしまう
 */
class OAuthAuthorize extends React.Component {
  constructor(props) {
    super(props)

    this.formRef = React.createRef()
  }
  /**
   * @override
   */
  componentDidMount() {
    if (this.formRef.current) {
      this.formRef.current.submit()
    }
  }

  /**
   * @override
   */
  render() {
    const hiddenValues = CRCR_AUTH_FORM_VALUES

    return (
      <div className="authorizeForm" style={{display: 'none'}}>
        <form action="/oauth/authorize" method="POST" ref={this.formRef}>
          {Object.entries(hiddenValues).map(([k, v]) => {
            return (
              <input type="hidden" name={k} value={v} key={k} />
            )
          })}
        </form>
      </div>
    )
  }
}


// init redux for public pages
/**
 * publicページ系のためのReducerを作る
 * @param  {[type]} history      [description]
 * @return {func}
 */
function makeReducer(history) {
  return combineReducers({
    page: require('src/reducers/page').default,
    router: connectRouter(history),
  })
}

/**
 * [configureStore description]
 * @param  {[type]} history      [description]
 * @param  {[type]} initialState [description]
 * @return {[type]}              [description]
 */
function configureStore(history, initialState) {
  const sagaMiddleware = createSagaMiddleware()

  const store = createStore(
    makeReducer(history),
    initialState,
    compose(
      applyMiddleware(routerMiddleware(history), sagaMiddleware),
    ),
  )
  store.runSaga = sagaMiddleware.run

  return store
}

const history = createBrowserHistory()
const store = configureStore(history, {})
store.runSaga(function* () {
  yield fork(require('src/sagas/snackbar').default)
})

// start react
render(
  <Provider store={store}>
    <MuiThemeProvider muiTheme={muiTheme}>
      <Router history={history}>
        <Route
          render={(props) => (
            <PublicFrame {...props}>
              <Switch>
                <Route exact path="/oauth/login" component={OAuthLogin} />
                <Route exact path="/oauth/authorize" component={OAuthAuthorize} />
                <Route exact path="/invitation/:linkUuid" component={UserInvitation} />
              </Switch>
            </PublicFrame>
          )}
        />
      </Router>
    </MuiThemeProvider>
  </Provider>,

  document.getElementById('app')
)
