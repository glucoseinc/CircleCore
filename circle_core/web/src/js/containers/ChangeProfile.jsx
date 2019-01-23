import PropTypes from 'prop-types'
import React from 'react'
import {connect} from 'react-redux'

import actions from 'src/actions'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'

import UserEditPaper from 'src/components/UserEditPaper'


/**
 * プロフィール変更
 */
class ChangeProfile extends React.Component {
  static propTypes = {
    isUserFetching: PropTypes.bool.isRequired,
    isUserUpdating: PropTypes.bool.isRequired,
    users: PropTypes.object.isRequired,
    errors: PropTypes.object,
    myID: PropTypes.string,
    onRenewTokenRequested: PropTypes.func,
    onUpdateClick: PropTypes.func,
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
      myID,
      onRenewTokenRequested,
      onUpdateClick,
    } = this.props

    if (isUserFetching || isUserUpdating) {
      return (
        <LoadingIndicator />
      )
    }

    const user = users.get(myID)

    if (user === undefined) {
      return (
        <div>
          {myID}は存在しません
        </div>
      )
    }

    return (
      <div className="page">
        <UserEditPaper
          user={user}
          errors={errors}
          canChangePermission={false}
          needCurrentPassword={true}
          onSaveClick={onUpdateClick}
          onRenewTokenRequested={onRenewTokenRequested}
        />
      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  isUserFetching: state.asyncs.isUserFetching,
  isUserUpdating: state.asyncs.isUserUpdating,
  users: state.entities.users,
  errors: state.error.userEdit,
  myID: state.entities.myID,
})

const mapDispatchToProps = (dispatch) => ({
  onRenewTokenRequested: (user) => {
    dispatch(actions.user.renewTokenRequest(user.uuid))
  },
  onUpdateClick: (user, currentPassword, newPassword) => {
    const rawUser = {
      ...user.toJS(),
      currentPassword,
      newPassword,
      permissions: undefined,
    }
    dispatch(actions.user.updateRequest(rawUser))
  },
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(ChangeProfile)
