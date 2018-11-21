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
    onOkClick: PropTypes.func.isRequired,
    onCancelClick: PropTypes.func.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      open = false,
      replicationLink,
      onOkClick,
      onCancelClick,
    } = this.props

    return (
      <DeleteDialog
        obj={replicationLink}
        title="この共有リンクを削除しますか？"
        onOkClick={onOkClick}
        onCancelClick={onCancelClick}
        open={open}
      />
    )
  }
}

export default ReplicationLinkDeleteDialog
