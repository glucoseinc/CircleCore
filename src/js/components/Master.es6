import React, {Component, PropTypes} from 'react'
import Title from 'react-title-component'
import AppBar from 'material-ui/AppBar'
import spacing from 'material-ui/styles/spacing'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import {darkWhite, lightWhite, grey900} from 'material-ui/styles/colors'
import withWidth, {MEDIUM, LARGE} from 'material-ui/utils/withWidth'

import AppNavDrawer from './AppNavDrawer'
import FullWidthSection from './FullWidthSection'


/**
 * サイト全体の枠
 */
class Master extends Component {
  static propTypes = {
    children: PropTypes.node,
    location: PropTypes.object,
    width: PropTypes.number.isRequired,
  }

  static contextTypes = {
    router: PropTypes.object.isRequired,
  }

  static childContextTypes = {
    muiTheme: PropTypes.object,
  }

  state = {
    navDrawerOpen: false,
  }

  /**
   * _TODO_DOC_HERE_
   * @return {Object} _TODO_DOC_HERE_
   */
  getChildContext() {
    return {
      muiTheme: this.state.muiTheme,
    }
  }

  /**
   * @override
   */
  componentWillMount() {
    this.setState({
      muiTheme: getMuiTheme(),
    })
  }

  /**
   * @override
   */
  componentWillReceiveProps(nextProps, nextContext) {
    const newMuiTheme = nextContext.muiTheme ? nextContext.muiTheme : this.state.muiTheme
    this.setState({
      muiTheme: newMuiTheme,
    })
  }

  /**
   * _TODO_DOC_HERE_
   * @return {Object} _TODO_DOC_HERE_
   */
  getStyles() {
    const styles = {
      appBar: {
        position: 'fixed',
        // Needed to overlap the examples
        zIndex: this.state.muiTheme.zIndex.appBar + 1,
        top: 0,
      },
      root: {
        paddingTop: spacing.desktopKeylineIncrement,
        minHeight: 400,
      },
      content: {
        margin: spacing.desktopGutter,
      },
      contentWhenMedium: {
        margin: `${spacing.desktopGutter * 2}px ${spacing.desktopGutter * 3}px`,
      },
      footer: {
        backgroundColor: grey900,
        textAlign: 'center',
      },
      a: {
        color: darkWhite,
      },
      p: {
        margin: '0 auto',
        padding: 0,
        color: lightWhite,
        maxWidth: 356,
      },
      browserstack: {
        display: 'flex',
        alignItems: 'flex-start',
        justifyContent: 'center',
        margin: '25px 15px 0',
        padding: 0,
        color: lightWhite,
        lineHeight: '25px',
        fontSize: 12,
      },
      browserstackLogo: {
        margin: '0 3px',
      },
      iconButton: {
        color: darkWhite,
      },
    }

    if (this.props.width === MEDIUM || this.props.width === LARGE) {
      styles.content = Object.assign(styles.content, styles.contentWhenMedium)
    }

    return styles
  }

  /**
   * @override
   */
  render() {
    const {
      location,
      children,
    } = this.props

    let {
      navDrawerOpen,
    } = this.state

    const {
      prepareStyles,
    } = this.state.muiTheme

    const styles = this.getStyles()
    const pageTitle =
      // router.isActive('/get-started') ? 'Get Started' :
      // router.isActive('/customization') ? 'Customization' :
      // router.isActive('/components') ? 'Components' :
      // router.isActive('/discover-more') ? 'Discover More' :
      ''

    let docked = false
    let showMenuIconButton = true

    if (this.props.width === LARGE) {
      docked = true
      navDrawerOpen = true
      showMenuIconButton = false

      styles.navDrawer = {
        zIndex: styles.appBar.zIndex - 1,
      }
      styles.root.paddingLeft = 256
      styles.footer.paddingLeft = 256
    }

    return (
      <div>
        <Title render="CircleCore" />
        <AppBar
          onLeftIconButtonTouchTap={::this.handleTouchTapLeftIconButton}
          title={pageTitle}
          zDepth={0}
          style={styles.appBar}
          showMenuIconButton={showMenuIconButton}
        />
        <div style={prepareStyles(styles.root)}>
          <div style={prepareStyles(styles.content)}>
            {React.cloneElement(children, {
              onChangeMuiTheme: this.handleChangeMuiTheme,
            })}
          </div>
        </div>
        <AppNavDrawer
          style={styles.navDrawer}
          location={location}
          docked={docked}
          onRequestChangeNavDrawer={::this.handleChangeRequestNavDrawer}
          onChangeList={::this.handleChangeList}
          open={navDrawerOpen}
        />
        <FullWidthSection style={styles.footer}>
          Footer
        </FullWidthSection>
      </div>
    )
  }

  // event handlers
  /**
   * _TODO_DOC_HERE_
   */
  handleTouchTapLeftIconButton() {
    this.setState({
      navDrawerOpen: !this.state.navDrawerOpen,
    })
  }

  /**
   * _TODO_DOC_HERE_
   * @param {Object} open _TODO_DOC_HERE_
   */
  handleChangeRequestNavDrawer(open) {
    this.setState({
      navDrawerOpen: open,
    })
  }

  /**
   * _TODO_DOC_HERE_
   * @param {Object} event _TODO_DOC_HERE_
   * @param {Object} value _TODO_DOC_HERE_
   */
  handleChangeList(event, value) {
    this.context.router.push(value)
    this.setState({
      navDrawerOpen: false,
    })
  }

  /**
   * _TODO_DOC_HERE_
   * @param {Object} muiTheme _TODO_DOC_HERE_
   */
  handleChangeMuiTheme(muiTheme) {
    this.setState({
      muiTheme: muiTheme,
    })
  }
}

export default withWidth()(Master)
