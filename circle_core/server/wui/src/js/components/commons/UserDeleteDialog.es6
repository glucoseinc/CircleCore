import React, {Component, PropTypes} from 'react'

import OkCancelDialog from 'src/components/bases/OkCancelDialog'


/**
 * User削除ダイアログ
 */
class UserDeleteDialog extends Component {
  static propTypes = {
    open: PropTypes.bool,
    user: PropTypes.object,
    onOkTouchTap: PropTypes.func.isRequired,
    onCancelTouchTap: PropTypes.func.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      open = false,
      user,
      onOkTouchTap,
      onCancelTouchTap,
    } = this.props

    return (
      <OkCancelDialog
        title="ユーザーを削除しますか？"
        okLabel="削除する"
        onOkTouchTap={() => onOkTouchTap(user)}
        cancelLabel="キャンセル"
        onCancelTouchTap={onCancelTouchTap}
        open={open}
      >
        <p>{user && user.displayName || ''}</p>
      </OkCancelDialog>
    )
  }
}

export default UserDeleteDialog
