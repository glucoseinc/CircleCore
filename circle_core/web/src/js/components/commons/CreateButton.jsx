import PropTypes from 'prop-types'
import React from 'react'

import CCRaisedButton from 'src/components/bases/CCRaisedButton'

import {AddIcon} from 'src/components/bases/icons'


/**
 * 作成ボタン
 */
class CreateButton extends React.Component {
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
      label = '追加する',
      disabled = false,
      onClick,
    } = this.props

    const style = {
      root: {
        minWidth: 160,
      },
      label: {
        paddingLeft: 0,
      },
    }

    return (
      <CCRaisedButton
        style={style.root}
        label={label}
        labelStyle={style.label}
        icon={AddIcon}
        primary={true}
        disabled={disabled}
        onClick={onClick}
      />
    )
  }
}

export default CreateButton
