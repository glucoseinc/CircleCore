/**
 * 認証がないページ用のReact
 *
 * main.es6は冒頭で認証チェックをしているので...
 */
import React from 'react'
import {render} from 'react-dom'
import {Router, Route, Link, browserHistory} from 'react-router'
import injectTapEventPlugin from 'react-tap-event-plugin'
import Title from 'react-title-component'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import AppBar from 'material-ui/AppBar'
import FlatButton from 'material-ui/FlatButton'
import TextField from 'material-ui/TextField'



injectTapEventPlugin()


class PublicFrame extends React.Component {
  render() {
    const {
    //   navDrawerOpen,
      children,
    //   width,
    //   actions,
    } = this.props
    // const {
    //   muiTheme,
    // } = this.context

    // const navDrawerAlwaysOpen = (width === LARGE)
    // const appBarShowMenuIconButton = navDrawerAlwaysOpen ? false : true

    return (
      <div className="container is-public">
        <Title render="Login"/>
        <div>
          <AppBar
            title="CircleCore"
            showMenuIconButton={false}
          />
          <div style={{}}>
            {children}
          </div>
        </div>
      </div>
    )
  }
}


class OAuthAuthorize extends React.Component {
  render() {
    const hiddenValues = CRCR_AUTH_FORM_VALUES

    return (
      <div className="authorizeForm" style={{margin: '0px auto', width: '320px'}}>

        <form action="/oauth/authorize" method="POST">

          {Object.entries(hiddenValues).map(([k, v]) => {
            return (
              <input type="hidden" name={k} value={v} key={k} />
            )
          })}

          <TextField
            hintText="アカウント"
            floatingLabelText="アカウント"
          /><br />

          <TextField
            hintText="パスワード"
            floatingLabelText="パスワード"
            type="password"
            /><br />

          <div className="authorizeForm-actions" style={{textAlign: 'right'}}>
            <FlatButton label="ログイン" primary={true} type="submit" />
          </div>
        </form>
      </div>
    )
  }
}


render(
  <MuiThemeProvider muiTheme={getMuiTheme()}>
    <Router history={browserHistory}>
      <Route path="/oauth" component={PublicFrame}>
        <Route path="authorize" component={OAuthAuthorize} />
      </Route>
    </Router>
  </MuiThemeProvider>,
  document.getElementById('app')
)
