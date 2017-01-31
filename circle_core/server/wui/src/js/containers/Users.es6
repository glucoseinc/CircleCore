import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'

import actions from 'src/actions'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'
import OkCancelDialog from 'src/components/bases/OkCancelDialog'

import UsersTable from 'src/components/UsersTable'


/**
 */
class Users extends Component {
  static propTypes = {
    isFetching: PropTypes.bool.isRequired,
    users: PropTypes.object.isRequired,
    token: PropTypes.object.isRequired,
    actions: PropTypes.object.isRequired,
  }

  /**
   * @constructor
   */
  constructor(...args) {
    super(...args)

    this.state = {
      // 削除対象のユーザ
      deleteTargetUser: null,
    }
  }

  /**
   * @override
   */
  render() {
    if(this.props.isFetching) {
      return (
        <LoadingIndicator />
      )
    }

    const {
      users,
      token,
    } = this.props

    const {
      deleteTargetUser,
    } = this.state

    const isReadOnly = token.hasScope('user+rw') ? false : true

    return (
      <div className="page">
        <UsersTable
          users={users}
          onDeleteUser={::this.onDeleteUser}
          readOnly={isReadOnly}
        />

        {deleteTargetUser &&
          <OkCancelDialog
            title="ユーザを削除しますか？"
            okLabel="削除する"
            onOkTouchTap={::this.onDeleteUserConfirmed}
            cancelLabel="キャンセル"
            onCancelTouchTap={() => this.setState({deleteTargetUser: null})}
            open={true}
          >
            <p>{`${deleteTargetUser.displayName} を削除しますか？`}</p>
          </OkCancelDialog>
        }
      </div>
    )
  }

  /**
   * ユーザの削除ボタンが押されたら呼ばれる
   * @param {User} user 削除対象ユーザ
   */
  onDeleteUser(user) {
    this.setState({
      deleteTargetUser: user,
    })
  }

  /**
   * ユーザーの削除確認でOKが押されたら呼ばれる
   */
  onDeleteUserConfirmed() {
    this.props.actions.users.deleteRequest(this.state.deleteTargetUser)
    this.setState({deleteTargetUser: null})
  }
}


/**
 * [mapStateToProps description]
 * @param  {[type]} state [description]
 * @return {[type]}       [description]
 */
function mapStateToProps(state) {
  return {
    isFetching: state.asyncs.isUsersFetching,
    users: state.entities.users,
    token: state.auth.token,
  }
}


/**
 * [mapDispatchToProps description]
 * @param  {[type]} dispatch [description]
 * @return {[type]}          [description]
 */
function mapDispatchToProps(dispatch) {
  return {
    actions: {
      users: bindActionCreators(actions.users, dispatch),
    },
  }
}


export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Users)
