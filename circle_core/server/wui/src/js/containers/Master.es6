import React, {PropTypes} from 'react'
import {connect} from 'react-redux'

import AppBar from 'material-ui/AppBar'
import Dialog from 'material-ui/Dialog'
import FlatButton from 'material-ui/FlatButton'
import Title from 'react-title-component'
import withWidth, {LARGE} from 'material-ui/utils/withWidth'

import actions from '../actions'
import NavDrawer from '../components/NavDrawer'
import {OAUTH_AUTHORIZATION_URL} from '../Authorization'
import DevTools from '../containers/DevTools'


/**
 * メインコンテンツ
 */
class Master extends React.Component {
  static propTypes = {
    title: PropTypes.string,
    errorMessage: PropTypes.string,
    children: PropTypes.node.isRequired,
    width: PropTypes.number.isRequired,
    onLocationChangeRequest: PropTypes.func,
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
  onNavDrawerMenutouchTap(pathname) {
    this.setState({
      navDrawerOpen: false,
    })
    this.props.onLocationChangeRequest(pathname)
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
      title,
      errorMessage,
      children,
      width,
    } = this.props
    const {
      muiTheme,
    } = this.context
    const showDevTool = false

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
        <div>
          <NavDrawer
            alwaysOpen={navDrawerAlwaysOpen}
            open={navDrawerOpen}
            onRequestChange={::this.onNavDrawerButtonTouchTap}
            onNavItemTouchTap={::this.onNavDrawerMenutouchTap}
          />
        </div>

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
  title: state.page.title,
  errorMessage: state.misc.errorMessage,
})

const mapDispatchToProps = (dispatch)=> ({
  onLocationChangeRequest: (pathname) => dispatch(actions.location.changeRequest(pathname)),
  onCloseErrorAlert: () => dispatch(actions.misc.clearErrorMessage()),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(withWidth()(Master))
