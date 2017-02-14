import React, {Component, PropTypes} from 'react'

import MoreIconMenu from './MoreIconMenu'


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
    }

    return (
      <div style={style.root}>
        <div style={style.children}>
          {children}
        </div>
        <MoreIconMenu>
          {React.Children.map(menuItems, (menuItem) => menuItem)}
        </MoreIconMenu>
      </div>
    )
  }
}


export default ComponentWithMoreIconMenu
