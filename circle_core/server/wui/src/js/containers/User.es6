import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'
import Title from 'react-title-component'
// import {bindActionCreators} from 'redux'
// import {put, take} from 'redux-saga/effects'
import {Snackbar} from 'material-ui'

// import actions, {actionTypes} from 'src/actions'
// import {store} from 'src/main'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'

import UserForm from 'src/components/UserForm'


/**
 * User情報の確認、編集
 */
class User extends Component {
  static propTypes = {
    isFetching: PropTypes.bool.isRequired,
    users: PropTypes.object.isRequired,
    token: PropTypes.object.isRequired,
    params: PropTypes.object.isRequired,
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
  render() {
    const {
      errors,
      openUpdatedSnackbar,
    } = this.state
    const {
      isFetching,
      users,
      token,
      params,
    } = this.props

    if (isFetching) {
      return (
        <LoadingIndicator />
      )
    }

    const user = users.get(params.userId)

    if (user === undefined) {
      // TODO: React-routerで404的なページに遷移できない?
      return (
        <div>
          {this.props.params.userId}は存在しません
        </div>
      )
    }

    const title = `ユーザー ${user.displayName}`

    return (
      <div className="page pageUserDetail">
        <Title render={(previousTitle) => `${title} - ${previousTitle}`} />

        <div className="markdown-body">
          <h2>{title}</h2>
        </div>

        <UserForm
          errors={errors}
          readOnly={token.hasScope('user+rw') ? false : true}
          user={user}
          onSubmitUserForm={this.onSubmitUserForm.bind(this, user)}
          />
        <Snackbar
          open={openUpdatedSnackbar}
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
    // const self = this

    // TODO(絶対使い方間違ってる.  create -> completeまで一貫性を持たせる方法が分からん...)
    // store.runSaga(function* () {
    //   yield put(actions.userOld.updateRequest({...params, uuid: user.uuid}))
    //   let {payload: {response, detail}} = yield take(actionTypes.userOld.updateComplete)
    //   if(response) {
    //     self.setState({openUpdatedSnackbar: true})
    //   } else {
    //     self.setState({errors: detail.errors})
    //     // alert(error.message)
    //   }
    // })
  }
}


const mapStateToProps = (state) => ({
  isFetching: state.asyncs.isUserFetching,
  users: state.entities.users,
  token: state.auth.token,
})

const mapDispatchToProps = (dispatch) => ({
  // actions: {
  //   users: bindActionCreators(actions.users, dispatch),
  // },
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(User)
