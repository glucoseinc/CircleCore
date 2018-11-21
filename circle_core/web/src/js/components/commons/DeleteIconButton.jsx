import PropTypes from 'prop-types'
import React from 'react'

import IconButton from 'material-ui/IconButton'

import {DeleteIcon} from 'src/components/bases/icons'


/**
 * 削除アイコンボタン
 */
class DeleteIconButton extends React.Component {
  static propTypes = {
    size: PropTypes.number,
    iconSize: PropTypes.number,
    disabled: PropTypes.bool,
    onClick: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      size = 24,
      iconSize = 24,
      disabled = false,
      onClick,
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
        onClick={onClick}
      >
        <DeleteIcon />
      </IconButton>
    )
  }
}

export default DeleteIconButton
