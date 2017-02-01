import React, {Component, PropTypes} from 'react'

import RaisedButton from 'material-ui/RaisedButton'

import {AddIcon} from 'src/components/bases/icons'


/**
 * 作成ボタン
 */
class CreateButton extends Component {
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
      label = '追加する',
      disabled = false,
      onTouchTap,
    } = this.props

    const style = {
      root: {
        minWidth: 160,
      },
      label: {
        paddingLeft: 0,
      },
      icon: {
        width: 16,
        height: 16,
      },
    }

    return (
      <RaisedButton
        style={style.root}
        label={label}
        labelStyle={style.label}
        icon={<AddIcon style={style.icon} />}
        primary={true}
        disabled={disabled}
        onTouchTap={onTouchTap}
       />
    )
  }
}

export default CreateButton