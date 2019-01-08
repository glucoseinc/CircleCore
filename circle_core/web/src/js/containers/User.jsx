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
      token,
      match: {
        params,
      },
      onUpdateClick,
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
        errors={errors}
        onSaveClick={onUpdateClick}
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
  errors: state.error.userEdit,
  token: state.auth.token,
})

const mapDispatchToProps = (dispatch) => ({
  onUpdateClick: (user, currentPassword, newPassword) => {
    dispatch(actions.user.updateRequest({...user.toJS(), newPassword}))
  },
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(User)
