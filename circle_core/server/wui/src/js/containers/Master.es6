import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'

import AppBar from 'material-ui/AppBar'
import Dialog from 'material-ui/Dialog'
import FlatButton from 'material-ui/FlatButton'
import Title from 'react-title-component'
import withWidth, {LARGE} from 'material-ui/utils/withWidth'

import actions from '../actions'
import NavDrawer from '../components/NavDrawer'
import DevTools from '../containers/DevTools'


/**
 */
class Master extends Component {
  static propTypes = {
    errorMessage: PropTypes.string,
    navDrawerOpen: PropTypes.bool.isRequired,
    children: PropTypes.node.isRequired,
    width: PropTypes.number.isRequired,
    actions: PropTypes.object.isRequired,
  }

  static contextTypes = {
    muiTheme: PropTypes.object.isRequired,
  }

  /**
   *@override
   */
  render() {
    const {
      errorMessage,
      navDrawerOpen,
      children,
      width,
      actions,
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
        padding: 20,
      },
    }

    return (
      <div>
        <Title render="CircleCore"/>
        <div style={style.content}>
          <AppBar
            showMenuIconButton={appBarShowMenuIconButton}
            onLeftIconButtonTouchTap={actions.misc.navDrawerToggleOpen}
          />
          <div style={style.children}>
            {children}
          </div>
        </div>
        <div>
          <NavDrawer
            alwaysOpen={navDrawerAlwaysOpen}
            open={navDrawerOpen}
            onRequestChange={actions.misc.navDrawerToggleOpen}
            onNavItemTouchTap={actions.location.changeRequest}
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

        <DevTools />
      </div>
    )
  }

  /**
   * エラーAlertの閉じるボタンが押された時に呼ばれる
   */
  onCloseErrorAlert() {
    //
    this.props.actions.misc.clearErrorMessage()
  }
}


/**
 * [mapStateToProps description]
 * @param  {[type]} state [description]
 * @return {[type]}       [description]
 */
function mapStateToProps(state) {
  return {
    navDrawerOpen: state.misc.navDrawerOpen,
    errorMessage: state.misc.errorMessage,
  }
}

/**
 * [mapDispatchToProps description]
 * @param  {[type]} dispatch [description]
 * @return {[type]}          [description]
 */
function mapDispatchToProps(dispatch) {
  return {
    actions: {
      location: bindActionCreators(actions.location, dispatch),
      misc: bindActionCreators(actions.misc, dispatch),
    },
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(withWidth()(Master))
