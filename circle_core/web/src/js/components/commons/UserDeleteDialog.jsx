import PropTypes from 'prop-types'
import React from 'react'

import DeleteDialog from 'src/components/commons/DeleteDialog'


/**
 * User削除ダイアログ
 */
class UserDeleteDialog extends React.Component {
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
      <DeleteDialog
        obj={user}
        title="このユーザーを削除しますか？"
        onOkTouchTap={onOkTouchTap}
        onCancelTouchTap={onCancelTouchTap}
        open={open}
      />
    )
  }
}

export default UserDeleteDialog
