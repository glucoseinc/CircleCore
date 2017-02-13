import React, {Component, PropTypes} from 'react'

import DeleteDialog from 'src/components/commons/DeleteDialog'


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
