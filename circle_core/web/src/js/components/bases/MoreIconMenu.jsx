import React, {Component, PropTypes} from 'react'

import IconButton from 'material-ui/IconButton'
import IconMenu from 'material-ui/IconMenu'

import {MoreIcon} from 'src/components/bases/icons'


/**
* 追加アイコンメニュー
*/
class MoreIconMenu extends Component {
  static propTypes = {
    style: PropTypes.object,
    children: PropTypes.node,
  }

  /**
   * @override
   */
  render() {
    const {
      children,
    } = this.props

    const style = {
      root: {
        display: 'block',
        position: 'absolute',
        right: 16,
        top: 16,
        zIndex: 10,
        ...(this.props.style || {}),
      },
      icon: {
        width: 24,
        height: 24,
      },
      button: {
        width: '100%',
        height: '100%',
        padding: 0,
        display: 'block',
      },
      moreIcon: {
        width: '100%',
        height: '100%',
        display: 'block',
      },
      list: {
        paddingTop: 0,
        paddingBottom: 0,
      },
      menuItemInnerDiv: {
        fontSize: 14,
        paddingLeft: 32,
        paddingRight: 8,
      },
      menuItemIcon: {
        margin: '16px 4px',
        width: 16,
        height: 16,
      },
    }

    return (
      <IconMenu
        className="moreIconMenu"
        style={style.root}
        iconButtonElement={
          <IconButton
            className="test-IconButton"
            style={style.button}
            iconStyle={style.icon}
          >
            <MoreIcon
              className="test-MoreIcon"
              style={style.moreIcon}
            />
          </IconButton>
        }
        anchorOrigin={{vertical: 'bottom', horizontal: 'right'}}
        targetOrigin={{vertical: 'top', horizontal: 'right'}}
        listStyle={style.list}
      >
        {React.Children.map(children, (menuItem) => {
          const innerDivStyle = style.menuItemInnerDiv
          const leftIcon = React.cloneElement(
            menuItem.props.leftIcon,
            {style: style.menuItemIcon},
          )
          return React.cloneElement(
            menuItem,
            {innerDivStyle, leftIcon},
          )
        })}
      </IconMenu>
    )
  }
}


export default MoreIconMenu
