import PropTypes from 'prop-types'
import React from 'react'

import CCRaisedButton from 'src/components/bases/CCRaisedButton'


/**
 * 保存ボタン
 */
class SaveButton extends React.Component {
  static propTypes = {
    label: PropTypes.string,
    disabled: PropTypes.bool,
    onTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      label = '保存する',
      disabled = false,
      onTouchTap,
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
        primary={true}
        disabled={disabled}
        onTouchTap={onTouchTap}
      />
    )
  }
}

export default SaveButton
