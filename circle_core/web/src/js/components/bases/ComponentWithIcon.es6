import React, {Component, PropTypes} from 'react'

import {grey400} from 'material-ui/styles/colors'


/**
 * アイコン付きコンポーネント
 */
class ComponentWithIcon extends Component {
  static propTypes = {
    icon: PropTypes.func.isRequired,
    children: PropTypes.node,
  }

  /**
   * @override
   */
  render() {
    const {
        icon,
        children,
    } = this.props

    const style = {
      root: {
        position: 'relative',
      },

      icon: {
        display: 'block',
        float: 'left',
        width: 16,
        height: 16,
      },

      children: {
        marginLeft: 24,
      },
    }

    const Icon = icon

    return (
      <div style={style.root}>
        <Icon style={style.icon} color={grey400}/>
        <div style={style.children}>
          {children}
        </div>
      </div>
    )
  }
}


export default ComponentWithIcon
