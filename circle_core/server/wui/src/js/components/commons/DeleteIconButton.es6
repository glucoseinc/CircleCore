import React, {Component, PropTypes} from 'react'

import IconButton from 'material-ui/IconButton'

import {DeleteIcon} from 'src/components/bases/icons'


/**
 * 削除アイコンボタン
 */
class DeleteIconButton extends Component {
  static propTypes = {
    size: PropTypes.number,
    iconSize: PropTypes.number,
    disabled: PropTypes.bool,
    onTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      size = 24,
      iconSize = 24,
      disabled = false,
      onTouchTap,
    } = this.props

    const style = {
      root: {
        width: size,
        height: size,
        padding: (size - iconSize) / 2,
      },
      icon: {
        width: iconSize,
        height: iconSize,
      },
    }
    return (
      <IconButton
        style={style.root}
        iconStyle={style.icon}
        disabled={disabled}
        onTouchTap={onTouchTap}
      >
        <DeleteIcon />
      </IconButton>
    )
  }
}

export default DeleteIconButton
