import React, {PropTypes} from 'react'
import {connect} from 'react-redux'
import Title from 'react-title-component'
import {bindActionCreators} from 'redux'
import {put, take} from 'redux-saga/effects'
import {Snackbar} from 'material-ui'

import actions, {actionTypes} from '../actions'
import Fetching from '../components/Fetching'
import UserForm from '../components/UserForm'
import {store} from '../main'


/**
 * User情報の確認、編集
 */
class User extends React.Component {
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
      errors: {},
      openUpdatedSnackbar: false,
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
    // const {
    // } = this.props

    const user = this.props.users.get(this.props.params.userId)
    if(!user) {
      // TODO: React-routerで404的なページに遷移できない?
      return (
        <div>
          {this.props.params.userId}は存在しません
        </div>
      )
    }

    const title = `ユーザー ${user.displayName}`

    return (
      <div className="page page-userDetail">
        <Title render={(previousTitle) => `${title} - ${previousTitle}`} />

        <div className="markdown-body">
          <h2>{title}</h2>
        </div>

        <UserForm
          errors={this.state.errors}
          readOnly={this.props.token.hasScope('user+rw') ? false : true}
          user={user}
          onSubmitUserForm={this.onSubmitUserForm.bind(this, user)}
          />
        <Snackbar
          open={this.state.openUpdatedSnackbar}
          message="ユーザー情報を変更しました。"
          autoHideDuration={2000}
          onRequestClose={() => this.setState({openUpdatedSnackbar: false})}
        />
      </div>
    )
  }

  /**
   * UserFormから送信する時に呼ばれる
   * @param {User} user
   * @param {Object} params form data
   */
  onSubmitUserForm(user, params) {
    // clear errors
    this.setState({errors: {}})

    // send update
    const self = this

    // TODO(絶対使い方間違ってる.  create -> completeまで一貫性を持たせる方法が分からん...)
    store.runSaga(function* () {
      yield put(actions.user.updateRequest({...params, uuid: user.uuid}))
      let {payload: {response, detail}} = yield take(actionTypes.user.updateComplete)
      if(response) {
        self.setState({openUpdatedSnackbar: true})
      } else {
        self.setState({errors: detail.errors})
        // alert(error.message)
      }
    })
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
)(User)
