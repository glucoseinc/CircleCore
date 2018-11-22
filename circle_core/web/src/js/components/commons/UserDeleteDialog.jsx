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
    onOkClick: PropTypes.func.isRequired,
    onCancelClick: PropTypes.func.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      open = false,
      user,
      onOkClick,
      onCancelClick,
    } = this.props

    return (
      <DeleteDialog
        obj={user}
        title="このユーザーを削除しますか？"
        onOkClick={onOkClick}
        onCancelClick={onCancelClick}
        open={open}
      />
    )
  }
}

export default UserDeleteDialog
