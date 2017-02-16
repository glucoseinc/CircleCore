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
      icon: {
        width: 24,
        height: 24,
        ...(this.props.style || {}),
      },
      button: {
        width: 24,
        height: 24,
        padding: 0,
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
      <div className="moreIconMenu" style={style.icon}>
        <IconMenu
          iconButtonElement={
            <IconButton
              style={style.button}
              iconStyle={style.icon}
            >
              <MoreIcon />
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
      </div>
    )
  }
}


export default MoreIconMenu
