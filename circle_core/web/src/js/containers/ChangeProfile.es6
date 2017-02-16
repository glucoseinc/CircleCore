import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'

import actions from 'src/actions'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'

import UserEditPaper from 'src/components/UserEditPaper'


/**
 * プロフィール変更
 */
class ChangeProfile extends Component {
  static propTypes = {
    isUserFetching: PropTypes.bool.isRequired,
    isUserUpdating: PropTypes.bool.isRequired,
    users: PropTypes.object.isRequired,
    myID: PropTypes.string,
    onUpdateTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      isUserFetching,
      isUserUpdating,
      users,
      myID,
      onUpdateTouchTap,
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
          needCurrentPassword={true}
          onSaveTouchTap={onUpdateTouchTap}
        />
      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  isUserFetching: state.asyncs.isUserFetching,
  isUserUpdating: state.asyncs.isUserUpdating,
  users: state.entities.users,
  myID: state.entities.myID,
})

const mapDispatchToProps = (dispatch) => ({
  onUpdateTouchTap: (user, currentPassword, newPassword) => {
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
