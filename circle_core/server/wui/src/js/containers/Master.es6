import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'
import {routerActions} from 'react-router-redux'

import AppBar from 'material-ui/AppBar'
import Dialog from 'material-ui/Dialog'
import FlatButton from 'material-ui/FlatButton'
import Snackbar from 'material-ui/Snackbar'
import Title from 'react-title-component'
import withWidth, {LARGE} from 'material-ui/utils/withWidth'

import actions from 'src/actions'
import {OAUTH_AUTHORIZATION_URL} from 'src/Authorization'

import NavDrawer from 'src/components/NavDrawer'
import DevTools from 'src/containers/DevTools'


/**
 * メインコンテンツ
 */
class Master extends Component {
  static propTypes = {
    isSnackbarOpen: PropTypes.bool,
    title: PropTypes.string,
    snackbarMessage: PropTypes.string,
    errorMessage: PropTypes.string,
    location: PropTypes.object.isRequired,
    children: PropTypes.node.isRequired,
    width: PropTypes.number.isRequired,
    onLocationChange: PropTypes.func,
    onSnackBarCloseRequest: PropTypes.func,
    onCloseErrorAlert: PropTypes.func,
  }

  static contextTypes = {
    muiTheme: PropTypes.object.isRequired,
  }

  state = {
    navDrawerOpen: false,
  }

  /**
   * NavDrawerの開閉
   * @param {bool} open
   */
  onNavDrawerButtonTouchTap(open) {
    this.setState({
      navDrawerOpen: open,
    })
  }

  /**
   * @param {string} pathname
   */
  onNavDrawerMenuTouchTap(pathname) {
    this.setState({
      navDrawerOpen: false,
    })
    if (pathname !== this.props.location.pathname) {
      this.props.onLocationChange(pathname)
    }
  }

  /**
   * エラーAlertの閉じるボタンが押された時に呼ばれる
   */
  onCloseErrorAlert() {
    this.props.onCloseErrorAlert()
  }

  /**
   *@override
   */
  render() {
    const {
      navDrawerOpen,
    } = this.state
    const {
      title = '',
      isSnackbarOpen = false,
      snackbarMessage = '',
      errorMessage,
      children,
      width,
      onSnackBarCloseRequest,
    } = this.props
    const {
      muiTheme,
    } = this.context
    const showDevTool = process.env.NODE_ENV === 'development'

    const navDrawerAlwaysOpen = (width === LARGE)
    const appBarShowMenuIconButton = navDrawerAlwaysOpen ? false : true

    const style = {
      content: {
        paddingLeft: navDrawerAlwaysOpen ? muiTheme.drawer.width : 0,
      },
      children: {
      },
    }

    return (
      <div>
        <Title render="CircleCore"/>
        <div style={style.content}>
          <AppBar
            title={title}
            showMenuIconButton={appBarShowMenuIconButton}
            onLeftIconButtonTouchTap={() => this.onNavDrawerButtonTouchTap(true)}
          />
          <div style={style.children}>
            {children}
          </div>
        </div>

        <NavDrawer
          alwaysOpen={navDrawerAlwaysOpen}
          open={navDrawerOpen}
          onRequestChange={::this.onNavDrawerButtonTouchTap}
          onNavItemTouchTap={::this.onNavDrawerMenuTouchTap}
        />

        <Snackbar
          open={isSnackbarOpen}
          message={snackbarMessage}
          autoHideDuration={4000}
          onRequestClose={onSnackBarCloseRequest}
        />

        {errorMessage != null &&
          <Dialog
            title="エラー"
            actions={<FlatButton label="閉じる" primary={true} onTouchTap={::this.onCloseErrorAlert} />}
            modal={true}
            open={errorMessage ? true : false}
            onRequestClose={::this.onCloseErrorAlert}
          >
            {errorMessage}
          </Dialog>
        }

        {showDevTool && <DevTools />}

      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  isSnackbarOpen: state.page.isSnackbarOpen,
  title: state.page.title,
  snackbarMessage: state.page.snackbarMessage,
  errorMessage: state.misc.errorMessage,
})

const mapDispatchToProps = (dispatch)=> ({
  onLocationChange: (pathname) => dispatch(routerActions.push(pathname)),
  onSnackBarCloseRequest: () => dispatch(actions.page.hideSnackbar()),
  onCloseErrorAlert: () => dispatch(actions.misc.clearErrorMessage()),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(withWidth()(Master))
