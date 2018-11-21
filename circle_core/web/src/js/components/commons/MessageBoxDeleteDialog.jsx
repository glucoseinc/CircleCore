import PropTypes from 'prop-types'
import React from 'react'

import DeleteDialog from 'src/components/commons/DeleteDialog'


/**
 * MessageBox削除ダイアログ
 */
class MessageBoxDeleteDialog extends React.Component {
  static propTypes = {
    open: PropTypes.bool,
    module: PropTypes.object.isRequired,
    messageBoxIndex: PropTypes.number.isRequired,
    onOkTouchTap: PropTypes.func.isRequired,
    onCancelTouchTap: PropTypes.func.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      open = false,
      module,
      messageBoxIndex,
      onOkTouchTap,
      onCancelTouchTap,
    } = this.props

    const messageBox = module.messageBoxes.get(messageBoxIndex)

    return (
      <DeleteDialog
        obj={messageBox}
        title="このメッセージボックスを削除しますか？"
        onOkTouchTap={() => onOkTouchTap(messageBoxIndex)}
        onCancelTouchTap={onCancelTouchTap}
        open={open}
      />
    )
  }
}

export default MessageBoxDeleteDialog
