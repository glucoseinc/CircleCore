import React, {Component, PropTypes} from 'react'

import IconButton from 'material-ui/IconButton'


/**
 * アイコンボタン付きコンポーネント
 */
class ComponentWithIconButton extends Component {
  static propTypes = {
    icon: PropTypes.func.isRequired,
    onIconButtonTouchTap: PropTypes.func,
    children: PropTypes.node,
  }

  /**
   * @override
   */
  render() {
    const {
        icon,
        onIconButtonTouchTap,
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
    }

    const Icon = icon

    return (
      <div style={style.root}>
        <div style={style.children}>
          {children}
        </div>
        <div style={style.icon}>
          <IconButton
            style={style.button}
            iconStyle={style.icon}
            onTouchTap={onIconButtonTouchTap}
          >
            <Icon />
          </IconButton>
        </div>
      </div>
    )
  }
}


export default ComponentWithIconButton
