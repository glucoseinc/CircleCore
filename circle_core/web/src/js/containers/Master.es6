import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'
import {routerActions} from 'react-router-redux'

import AppBar from 'material-ui/AppBar'
import Snackbar from 'material-ui/Snackbar'
import Title from 'react-title-component'
import withWidth, {LARGE} from 'material-ui/utils/withWidth'

import actions from 'src/actions'

import ErrorDialog from 'src/components/ErrorDialog'
import NavDrawer from 'src/components/NavDrawer'

import DevTools from 'src/containers/DevTools'


/**
 * メインコンテンツ
 */
class Master extends Component {
  static propTypes = {
    title: PropTypes.string,
    isSnackbarOpen: PropTypes.bool,
    snackbarMessage: PropTypes.string,
    isErrorDialogOpen: PropTypes.bool,
    errorDialogMessages: PropTypes.object,
    location: PropTypes.object.isRequired,
    children: PropTypes.node.isRequired,
    width: PropTypes.number.isRequired,
    onLocationChange: PropTypes.func,
    onSnackBarCloseRequest: PropTypes.func,
    onErrorDialogCloseRequest: PropTypes.func,
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
      onSnackBarCloseRequest,
      isErrorDialogOpen = false,
      onErrorDialogCloseRequest,
      errorDialogMessages = {},
      children,
      width,
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
        <Title render="CircleCore" />
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

        <ErrorDialog
          open={isErrorDialogOpen}
          messages={errorDialogMessages}
          onCloseRequest={onErrorDialogCloseRequest}
        />

        {showDevTool && <DevTools />}

      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  title: state.page.title,
  isSnackbarOpen: state.page.isSnackbarOpen,
  snackbarMessage: state.page.snackbarMessage,
  isErrorDialogOpen: state.page.isErrorDialogOpen,
  errorDialogMessages: state.page.errorDialogMessages,
})

const mapDispatchToProps = (dispatch)=> ({
  onLocationChange: (pathname) => dispatch(routerActions.push(pathname)),
  onSnackBarCloseRequest: () => dispatch(actions.page.hideSnackbar()),
  onErrorDialogCloseRequest: () => dispatch(actions.page.hideErrorDialog()),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(withWidth()(Master))
