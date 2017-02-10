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
 * 自分の情報の確認、編集
 */
class ChangeProfile extends Component {
  static propTypes = {
    isFetching: PropTypes.bool.isRequired,
    myID: PropTypes.string,
    users: PropTypes.object,
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
      myID,
      users,
    } = this.props

    if (isFetching) {
      return (
        <LoadingIndicator />
      )
    }

    const user = users.get(myID)
    const title = 'プロフィール変更ユーザー'

    return (
      <div className="page page-changeProfile">
        <Title render={(previousTitle) => `${title} - ${previousTitle}`} />

        <UserForm
          errors={errors}
          readOnly={false}
          user={user}
          showCurrentPasswordFiled={true}
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
    // TODO(Userの関数と同じ... actionに切り出せ)
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
  myID: state.entities.myID,
  users: state.entities.users,
})

const mapDispatchToProps = (dispatch) => ({
    // actions: {
    //   users: bindActionCreators(actions.users, dispatch),
    // },
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(ChangeProfile)
