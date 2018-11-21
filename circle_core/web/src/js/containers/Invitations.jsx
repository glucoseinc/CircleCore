import PropTypes from 'prop-types'
import React from 'react'
import {connect} from 'react-redux'

import actions from 'src/actions'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'
import {InvitationIcon} from 'src/components/bases/icons'

import AddFloatingActionButton from 'src/components/commons/AddFloatingActionButton'
import InvitationCreatedDialog from 'src/components/commons/InvitationCreatedDialog'
import InvitationDeleteDialog from 'src/components/commons/InvitationDeleteDialog'

import Empty from 'src/components/Empty'
import InvitationInfoPaper from 'src/components/InvitationInfoPaper'


/**
 * Invitation一覧
 */
class Invitations extends React.Component {
  static propTypes = {
    isInvitationCreating: PropTypes.bool.isRequired,
    isInvitationFetching: PropTypes.bool.isRequired,
    isInvitationCreatedDialogOpen: PropTypes.bool.isRequired,
    invitations: PropTypes.object.isRequired,
    newInvitation: PropTypes.object,
    token: PropTypes.object.isRequired,
    onCreateClick: PropTypes.func,
    onCreatedDialogClose: PropTypes.func,
    onDeleteOkButtonClick: PropTypes.func,
  }

  state = {
    deleteInvitation: null,
    isInvitationDeleteDialogOpen: false,
  }

  /**
   * 追加メニュー 削除の選択時の動作
   * @param {object} invitation
   */
  onDeleteClick(invitation) {
    this.setState({
      deleteInvitation: invitation,
      isInvitationDeleteDialogOpen: true,
    })
  }

  /**
   * 削除ダイアログのボタン押下時の動作
   * @param {bool} execute
   * @param {object} invitation
   */
  onDeleteDialogButtonClick(execute, invitation) {
    this.setState({
      deleteInvitation: null,
      isInvitationDeleteDialogOpen: false,
    })
    if (execute && invitation) {
      this.props.onDeleteOkButtonClick(invitation)
    }
  }

  /**
   * @override
   */
  render() {
    const {
      deleteInvitation,
      isInvitationDeleteDialogOpen,
    } = this.state
    const {
      isInvitationCreating,
      isInvitationFetching,
      isInvitationCreatedDialogOpen,
      invitations,
      newInvitation,
      token,
      onCreateClick,
      onCreatedDialogClose,
    } = this.props

    if (isInvitationCreating || isInvitationFetching) {
      return (
        <LoadingIndicator />
      )
    }

    const isReadOnly = token.hasScope('user+rw') ? false : true

    return (
      <div>
        {invitations.size === 0 ? (
          <Empty
            icon={InvitationIcon}
            itemName="招待リンク"
          />
        ) : (
          <div className="page">
            {invitations.valueSeq().map((invitation) => (
              <InvitationInfoPaper
                key={invitation.uuid}
                invitation={invitation}
                readOnly={isReadOnly}
                onDeleteClick={::this.onDeleteClick}
              />
            ))}
          </div>
        )}

        <AddFloatingActionButton
          onClick={onCreateClick}
        />

        <InvitationCreatedDialog
          open={isInvitationCreatedDialogOpen}
          invitation={newInvitation}
          onClick={onCreatedDialogClose}
        />

        <InvitationDeleteDialog
          open={isInvitationDeleteDialogOpen}
          invitation={deleteInvitation}
          onOkClick={(invitation) => this.onDeleteDialogButtonClick(true, invitation)}
          onCancelClick={() => this.onDeleteDialogButtonClick(false)}
        />
      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  isInvitationCreating: state.asyncs.isInvitationCreating,
  isInvitationFetching: state.asyncs.isInvitationFetching,
  isInvitationCreatedDialogOpen: state.misc.isInvitationCreatedDialogOpen,
  invitations: state.entities.invitations,
  newInvitation: state.misc.newInvitation,
  token: state.auth.token,
})

const mapDispatchToProps = (dispatch) => ({
  onCreateClick: () => dispatch(actions.invitation.createRequest({maxInvites: 1})),
  onCreatedDialogClose: () => dispatch(actions.invitation.createdDialogClose()),
  onDeleteOkButtonClick: (invitation) => dispatch(actions.invitation.deleteRequest(invitation.uuid)),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Invitations)
