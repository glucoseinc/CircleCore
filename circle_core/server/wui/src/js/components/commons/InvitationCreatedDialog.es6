import React, {Component, PropTypes} from 'react'

import OkDialog from 'src/components/bases/OkDialog'


/**
* Invitation作成完了ダイアログ
*/
class InvitationCreatedDialog extends Component {
  static propTypes = {
    open: PropTypes.bool,
    invitation: PropTypes.object,
    onTouchTap: PropTypes.func.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      invitation,
      open = false,
      onTouchTap,
    } = this.props

    if (invitation === undefined || invitation === null) {
      return null
    }

    return (
      <OkDialog
        title="招待リンクを作成しました"
        label="閉じる"
        onTouchTap={onTouchTap}
        open={open}
      >
        <p>{invitation.url}</p>
        <p>このURLを招待したいユーザーに教えてください</p>
      </OkDialog>
    )
  }
}


export default InvitationCreatedDialog
