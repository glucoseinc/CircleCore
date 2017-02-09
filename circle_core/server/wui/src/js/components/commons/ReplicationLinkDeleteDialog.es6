import React, {Component, PropTypes} from 'react'

import OkCancelDialog from 'src/components/bases/OkCancelDialog'


/**
 * ReplicationLink削除ダイアログ
 */
class ReplicationLinkDeleteDialog extends Component {
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
      <OkCancelDialog
        title="共有リンクを削除しますか？"
        okLabel="削除する"
        onOkTouchTap={() => onOkTouchTap(replicationLink)}
        cancelLabel="キャンセル"
        onCancelTouchTap={onCancelTouchTap}
        open={open}
      >
        <p>{replicationLink && replicationLink.label || ''}</p>
      </OkCancelDialog>
    )
  }
}

export default ReplicationLinkDeleteDialog
