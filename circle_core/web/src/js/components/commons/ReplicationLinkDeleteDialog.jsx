import PropTypes from 'prop-types'
import React from 'react'

import DeleteDialog from 'src/components/commons/DeleteDialog'


/**
 * ReplicationLink削除ダイアログ
 */
class ReplicationLinkDeleteDialog extends React.Component {
  static propTypes = {
    open: PropTypes.bool,
    replicationLink: PropTypes.object,
    onOkTouchTap: PropTypes.func.isRequired,
    onCancelTouchTap: PropTypes.func.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      open = false,
      replicationLink,
      onOkTouchTap,
      onCancelTouchTap,
    } = this.props

    return (
      <DeleteDialog
        obj={replicationLink}
        title="この共有リンクを削除しますか？"
        onOkTouchTap={onOkTouchTap}
        onCancelTouchTap={onCancelTouchTap}
        open={open}
      />
    )
  }
}

export default ReplicationLinkDeleteDialog
