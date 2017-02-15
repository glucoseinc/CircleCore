import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'

import actions from 'src/actions'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'

import UserDetail from 'src/components/UserDetail'
import UserEditPaper from 'src/components/UserEditPaper'


/**
 * User詳細
 */
class User extends Component {
  static propTypes = {
    isUserFetching: PropTypes.bool.isRequired,
    isUserUpdating: PropTypes.bool.isRequired,
    users: PropTypes.object.isRequired,
    token: PropTypes.object.isRequired,
    params: PropTypes.object.isRequired,
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
      token,
      params,
      onUpdateTouchTap,
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

    const userDetail = token.hasScope('user+rw') ? (
      <UserEditPaper
        user={user}
        onSaveTouchTap={onUpdateTouchTap}
      />
    ) : (
      <UserDetail
        user={user}
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
  token: state.auth.token,
})

const mapDispatchToProps = (dispatch) => ({
  onUpdateTouchTap: (user, currentPassword, newPassword) => {
    dispatch(actions.user.updateRequest({...user.toJS(), newPassword}))
  },
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(User)
