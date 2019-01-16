import PropTypes from 'prop-types'
import React from 'react'
import {connect} from 'react-redux'

import actions from 'src/actions'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'

import UserDetail from 'src/components/UserDetail'
import UserEditPaper from 'src/components/UserEditPaper'


/**
 * User詳細
 */
class User extends React.Component {
  static propTypes = {
    isUserFetching: PropTypes.bool.isRequired,
    isUserUpdating: PropTypes.bool.isRequired,
    users: PropTypes.object.isRequired,
    errors: PropTypes.object,
    token: PropTypes.object.isRequired,
    match: PropTypes.object.isRequired,
    myID: PropTypes.string,
    onUpdateClick: PropTypes.func,
    onRenewTokenRequested: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      isUserFetching,
      isUserUpdating,
      users,
      errors = {},
      token,
      match: {
        params,
      },
      myID,
      onUpdateClick,
      onRenewTokenRequested,
    } = this.props

    if (isUserFetching || isUserUpdating) {
      return (
        <LoadingIndicator />
      )
    }

    const user = users.get(params.userId)

    if (user === undefined) {
      return (
        <div>
          {params.userId}は存在しません
        </div>
      )
    }

    const isMe = (myID === user.uuid)
    const userDetail = token.hasScope('user+rw') ? (
      <UserEditPaper
        user={user}
        errors={errors}
        onSaveClick={onUpdateClick}
        onRenewTokenRequested={onRenewTokenRequested}
      />
    ) : (
      <UserDetail
        user={user}
        isMe={isMe}
        onRenewTokenRequested={isMe && onRenewTokenRequested}
      />
    )

    return (
      <div className="page">
        {userDetail}
      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  isUserFetching: state.asyncs.isUserFetching,
  isUserUpdating: state.asyncs.isUserUpdating,
  users: state.entities.users,
  errors: state.error.userEdit,
  token: state.auth.token,
  myID: state.entities.myID,
})

const mapDispatchToProps = (dispatch) => ({
  onUpdateClick: (user, currentPassword, newPassword) => {
    dispatch(actions.user.updateRequest({...user.toJS(), newPassword}))
  },
  onRenewTokenRequested: (user) => {
    dispatch(actions.user.renewTokenRequest(user.uuid))
  },
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(User)
