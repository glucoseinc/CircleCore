import PropTypes from 'prop-types'
import React from 'react'

import DeleteDialog from 'src/components/commons/DeleteDialog'


/**
 * Invitation削除ダイアログ
 */
class InvitationDeleteDialog extends React.Component {
  static propTypes = {
    open: PropTypes.bool,
    invitation: PropTypes.object,
    onOkTouchTap: PropTypes.func.isRequired,
    onCancelTouchTap: PropTypes.func.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      open,
      invitation,
      onOkTouchTap,
      onCancelTouchTap,
    } = this.props

    return (
      <DeleteDialog
        obj={invitation}
        primaryLabelName="url"
        title="この招待リンクを削除しますか？"
        onOkTouchTap={onOkTouchTap}
        onCancelTouchTap={onCancelTouchTap}
        open={open}
      />
    )
  }
}

export default InvitationDeleteDialog
