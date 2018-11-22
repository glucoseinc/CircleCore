import PropTypes from 'prop-types'
import React from 'react'

import OkDialog from 'src/components/bases/OkDialog'


/**
* Invitation作成完了ダイアログ
*/
class InvitationCreatedDialog extends React.Component {
  static propTypes = {
    open: PropTypes.bool,
    invitation: PropTypes.object,
    onClick: PropTypes.func.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      invitation,
      open = false,
      onClick,
    } = this.props

    if (invitation === undefined || invitation === null) {
      return null
    }

    return (
      <OkDialog
        title="招待リンクを作成しました"
        label="閉じる"
        onClick={onClick}
        open={open}
      >
        <p>{invitation.url}</p>
        <p>このURLを招待したいユーザーに教えてください</p>
      </OkDialog>
    )
  }
}


export default InvitationCreatedDialog
