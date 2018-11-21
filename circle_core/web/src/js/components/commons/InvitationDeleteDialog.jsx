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
    onOkClick: PropTypes.func.isRequired,
    onCancelClick: PropTypes.func.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      open,
      invitation,
      onOkClick,
      onCancelClick,
    } = this.props

    return (
      <DeleteDialog
        obj={invitation}
        primaryLabelName="url"
        title="この招待リンクを削除しますか？"
        onOkClick={onOkClick}
        onCancelClick={onCancelClick}
        open={open}
      />
    )
  }
}

export default InvitationDeleteDialog
