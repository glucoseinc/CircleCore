import React, {Component, PropTypes} from 'react'

import IconButton from 'material-ui/IconButton'
import ActionDelete from 'material-ui/svg-icons/action/delete'


/**
 * 削除アイコンボタン
 */
class DeleteIconButton extends Component {
  static propTypes = {
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
        <ActionDelete />
      </IconButton>
    )
  }
}

export default DeleteIconButton
