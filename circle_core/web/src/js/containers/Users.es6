import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'
import {routerActions} from 'react-router-redux'

import actions from 'src/actions'
import {urls, createPathName} from 'src/routes'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'
import {UserIcon} from 'src/components/bases/icons'

import UserDeleteDialog from 'src/components/commons/UserDeleteDialog'

import Empty from 'src/components/Empty'
import UsersTableComponent from 'src/components/UsersTableComponent'


/**
 * User一覧
 */
class Users extends Component {
  static propTypes = {
    isUserFetching: PropTypes.bool.isRequired,
    users: PropTypes.object.isRequired,
    myID: PropTypes.string,
    token: PropTypes.object.isRequired,
    onDisplayNameTouchTap: PropTypes.func,
    onDeleteOkButtonTouchTap: PropTypes.func,
  }

  state = {
    deleteUser: null,
    isUserDeleteDialogOpen: false,
  }

  /**
   * 追加メニュー 削除の選択時の動作
   * @param {object} user
   */
  onDeleteTouchTap(user) {
    this.setState({
      deleteUser: user,
      isUserDeleteDialogOpen: true,
    })
  }

  /**
   * 削除ダイアログのボタン押下時の動作
   * @param {bool} execute
   * @param {object} user
   */
  onDeleteDialogButtonTouchTap(execute, user) {
    this.setState({
      deleteUser: null,
      isUserDeleteDialogOpen: false,
    })
    if (execute && user) {
      this.props.onDeleteOkButtonTouchTap(user)
    }
  }


  /**
   * @override
   */
  render() {
    const {
      deleteUser,
      isUserDeleteDialogOpen,
    } = this.state
    const {
      isUserFetching,
      users,
      myID,
      token,
      onDisplayNameTouchTap,
    } = this.props

    if (isUserFetching) {
      return (
        <LoadingIndicator />
      )
    }

    const isReadOnly = token.hasScope('user+rw') ? false : true

    return (
      <div>
        {users.size === 0 ? (
          <Empty
            icon={UserIcon}
            itemName="ユーザー"
          />
        ) : (
          <div className="page">
            <UsersTableComponent
              users={users}
              myID={myID}
              readOnly={isReadOnly}
              onDisplayNameTouchTap={(user) => onDisplayNameTouchTap(user.uuid)}
              onDeleteTouchTap={(user) => this.onDeleteTouchTap(user)}
            />
          </div>
        )}

        <UserDeleteDialog
          open={isUserDeleteDialogOpen}
          user={deleteUser}
          onOkTouchTap={(user) => this.onDeleteDialogButtonTouchTap(true, user)}
          onCancelTouchTap={() => this.onDeleteDialogButtonTouchTap(false)}
        />
      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  isUserFetching: state.asyncs.isUserFetching,
  users: state.entities.users,
  myID: state.entities.myID,
  token: state.auth.token,
})


const mapDispatchToProps = (dispatch) => ({
  onDisplayNameTouchTap: (userId) => dispatch(routerActions.push(createPathName(urls.user, {userId}))),
  onDeleteOkButtonTouchTap: (user) => dispatch(actions.user.deleteRequest(user.uuid)),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Users)
