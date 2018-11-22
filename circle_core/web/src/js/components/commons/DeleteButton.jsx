import PropTypes from 'prop-types'
import React from 'react'

import CCRaisedButton from 'src/components/bases/CCRaisedButton'


/**
 * 削除ボタン
 */
class DeleteButton extends React.Component {
  static propTypes = {
    label: PropTypes.string,
    disabled: PropTypes.bool,
    onClick: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      label = '削除する',
      disabled = false,
      onClick,
    } = this.props

    const style = {
      root: {
        minWidth: 160,
      },
    }

    return (
      <CCRaisedButton
        style={style.root}
        label={label}
        disabled={disabled}
        onClick={onClick}
      />
    )
  }
}

export default DeleteButton
