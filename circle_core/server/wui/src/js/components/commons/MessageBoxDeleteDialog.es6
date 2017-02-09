import React, {Component, PropTypes} from 'react'

import OkCancelDialog from 'src/components/bases/OkCancelDialog'


/**
 * MessageBox削除ダイアログ
 */
class MessageBoxDeleteDialog extends Component {
  static propTypes = {
    open: PropTypes.bool,
    module: PropTypes.object,
    messageBoxIndex: PropTypes.number,
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

    const messageBox = module && messageBoxIndex && module.messageBoxes.get(messageBoxIndex)

    return (
      <OkCancelDialog
        title="メッセージボックスを削除しますか？"
        okLabel="削除する"
        onOkTouchTap={() => onOkTouchTap(messageBoxIndex)}
        cancelLabel="キャンセル"
        onCancelTouchTap={onCancelTouchTap}
        open={open}
      >
        <p>{messageBox && messageBox.label || ''}</p>
      </OkCancelDialog>
    )
  }
}

export default MessageBoxDeleteDialog
