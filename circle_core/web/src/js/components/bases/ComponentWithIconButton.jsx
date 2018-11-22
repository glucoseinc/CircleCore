import PropTypes from 'prop-types'
import React from 'react'

import IconButton from 'material-ui/IconButton'


/**
 * アイコンボタン付きコンポーネント
 */
class ComponentWithIconButton extends React.Component {
  static propTypes = {
    rootStyle: PropTypes.object,
    childrenStyle: PropTypes.object,
    icon: PropTypes.func.isRequired,
    iconButtonDisabled: PropTypes.bool,
    onIconButtonClick: PropTypes.func,
    children: PropTypes.node,
  }

  /**
   * @override
   */
  render() {
    const {
      rootStyle = {},
      childrenStyle = {},
      icon,
      iconButtonDisabled = false,
      onIconButtonClick,
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

    const mergedRootStyle = {
      ...style.root,
      ...rootStyle,
    }

    const mergedChildrenStyle = {
      ...style.children,
      ...childrenStyle,
    }

    const Icon = icon

    return (
      <div style={mergedRootStyle}>
        <div style={mergedChildrenStyle}>
          {children}
        </div>
        <div style={style.icon}>
          <IconButton
            style={style.button}
            iconStyle={style.icon}
            disabled={iconButtonDisabled}
            onClick={onIconButtonClick}
          >
            <Icon />
          </IconButton>
        </div>
      </div>
    )
  }
}


export default ComponentWithIconButton
