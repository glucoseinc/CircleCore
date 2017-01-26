import React, {Component, PropTypes} from 'react'

import RaisedButton from 'material-ui/RaisedButton'


/**
 * 削除ボタン
 */
class DeleteButton extends Component {
  static propTypes = {
    disabled: PropTypes.bool,
    onTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      disabled = false,
      onTouchTap,
    } = this.props

    const style = {
      root: {
        minWidth: 160,
      },
    }

    return (
      <RaisedButton
        style={style.root}
        label="削除する"
        disabled={disabled}
        onTouchTap={onTouchTap}
       />
    )
  }
}

export default DeleteButton
