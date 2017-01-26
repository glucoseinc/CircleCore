import React, {Component, PropTypes} from 'react'

import IconButton from 'material-ui/IconButton'
import IconMenu from 'material-ui/IconMenu'
import NavigarionMoreVert from 'material-ui/svg-icons/navigation/more-vert'


/**
 * 追加アイコンメニュー付きコンポーネント
 */
class ComponentWithMoreIconMenu extends Component {
  static propTypes = {
    menuItems: PropTypes.node,
    children: PropTypes.node,
  }

  /**
   * @override
   */
  render() {
    const {
      menuItems,
      children,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'row nowrap',
        width: '100%',
      },

      children: {
        flexGrow: 1,
      },

      icon: {
        width: 24,
        height: 24,
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
      <div style={style.root}>
        <div style={style.children}>
          {children}
        </div>
        <div style={style.icon}>
          <IconMenu
            iconButtonElement={
              <IconButton
                style={style.button}
                iconStyle={style.icon}
              >
                <NavigarionMoreVert />
              </IconButton>
            }
            anchorOrigin={{vertical: 'bottom', horizontal: 'right'}}
            targetOrigin={{vertical: 'top', horizontal: 'right'}}
            listStyle={style.list}
          >
            {React.Children.map(menuItems, (menuItem) => {
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
      </div>
    )
  }
}


export default ComponentWithMoreIconMenu
