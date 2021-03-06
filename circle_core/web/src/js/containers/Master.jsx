import {routerActions} from 'connected-react-router'
import PropTypes from 'prop-types'
import React from 'react'
import {connect} from 'react-redux'

import AppBar from 'material-ui/AppBar'
import Snackbar from 'material-ui/Snackbar'
import Title from '@shnjp/react-title-component'
import withWidth, {LARGE} from 'material-ui/utils/withWidth'

import actions from 'src/actions'

import ErrorDialog from 'src/components/ErrorDialog'
import NavDrawer from 'src/components/NavDrawer'


/**
 * メインコンテンツ
 */
class Master extends React.Component {
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
    history: PropTypes.object.isRequired,
    match: PropTypes.object.isRequired,
    onActionRequest: PropTypes.func,
    onCcInfoFetchMyselfRequest: PropTypes.func,
    onSetTitleRequest: PropTypes.func,
    onUserFetchMyselfRequest: PropTypes.func,
    route: PropTypes.object.isRequired,
  }

  static contextTypes = {
    muiTheme: PropTypes.object.isRequired,
  }

  state = {
    navDrawerOpen: false,
  }

  /**
   *@override
   */
  componentDidMount() {
    const {
      onCcInfoFetchMyselfRequest,
      onUserFetchMyselfRequest,
    } = this.props

    onCcInfoFetchMyselfRequest()
    onUserFetchMyselfRequest()
    this.onRouteChanged()
  }

  /**
   *@override
   */
  componentDidUpdate(prevProps) {
    if (prevProps.route !== this.props.route) {
      this.onRouteChanged()
    }
  }

  /**
   * props.route change時の動作
   */
  onRouteChanged = () => {
    const {
      match: {
        params,
      },
      route: {
        label,
        onEnterActions,
      },
      onSetTitleRequest,
      onActionRequest,
    } = this.props

    onSetTitleRequest(label)
    if (onEnterActions !== undefined) {
      onEnterActions.map((action) => {
        onActionRequest(action, params)
      })
    }
  }

  /**
   * NavDrawerの開閉
   * @param {bool} open
   */
  onNavDrawerButtonClick(open) {
    this.setState({
      navDrawerOpen: open,
    })
  }

  /**
   * @param {string} pathname
   */
  onNavDrawerMenuItemClick(pathname) {
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
      location,
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
            onLeftIconButtonClick={() => this.onNavDrawerButtonClick(true)}
          />
          <div style={style.children}>
            {children}
          </div>
        </div>

        <NavDrawer
          alwaysOpen={navDrawerAlwaysOpen}
          open={navDrawerOpen}
          location={location}
          onRequestChange={::this.onNavDrawerButtonClick}
          onNavItemClick={::this.onNavDrawerMenuItemClick}
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
  onActionRequest: (action, params) => dispatch(action(params)),
  onCcInfoFetchMyselfRequest: () => dispatch(actions.ccInfo.fetchMyselfRequest()),
  onSetTitleRequest: (title) => dispatch(actions.page.setTitle(title)),
  onUserFetchMyselfRequest: () => dispatch(actions.user.fetchMyselfRequest()),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(withWidth()(Master))
