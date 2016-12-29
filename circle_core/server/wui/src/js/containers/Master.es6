import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'

import AppBar from 'material-ui/AppBar'
import withWidth, {LARGE} from 'material-ui/utils/withWidth'
import Title from 'react-title-component'

import NavDrawer from '../components/NavDrawer'
import DevTools from '../containers/DevTools'
import * as actions from '../actions/master'


/**
 */
class Master extends Component {
  static propTypes = {
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
            onLeftIconButtonTouchTap={actions.leftIconButtonTouchTap}
          />
          <div style={style.children}>
            {children}
          </div>
        </div>
        <div>
          <NavDrawer
            alwaysOpen={navDrawerAlwaysOpen}
            open={navDrawerOpen}
            onRequestChange={actions.navDrawerRequestChange}
            onNavItemTouchTap={actions.locationRequestChange}
          />
        </div>
        <DevTools />
      </div>
    )
  }
}


/**
 * [mapStateToProps description]
 * @param  {[type]} state [description]
 * @return {[type]}       [description]
 */
function mapStateToProps(state) {
  return {
    navDrawerOpen: state.miscs.navDrawerOpen,
  }
}

/**
 * [mapDispatchToProps description]
 * @param  {[type]} dispatch [description]
 * @return {[type]}          [description]
 */
function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(actions, dispatch),
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(withWidth()(Master))
