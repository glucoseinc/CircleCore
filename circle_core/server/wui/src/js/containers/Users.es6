import React, {PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'

import actions from '../actions'
import Fetching from '../components/Fetching'
import UsersTable from '../components/UsersTable'
import OkCancelDialog from '../components/OkCancelDialog'


/**
 */
class Users extends React.Component {
  static propTypes = {
    isFetching: PropTypes.bool.isRequired,
    users: PropTypes.array.isRequired,
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
  componentWillMount() {
    const {
      actions,
    } = this.props
    actions.users.fetchRequest()
  }

  /**
   * @override
   */
  render() {
    if(this.props.isFetching) {
      return (
        <Fetching />
      )
    }

    const {
      users,
    } = this.props

    const {
      deleteTargetUser,
    } = this.state

    return (
      <div>
        <UsersTable
          users={users}
          onDeleteUser={::this.onDeleteUser}
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
