import {Checkbox, IconButton, FlatButton, FontIcon, TextField, RaisedButton, Snackbar} from 'material-ui'
import React, {PropTypes} from 'react'
import {connect} from 'react-redux'
import Title from 'react-title-component'
import {bindActionCreators} from 'redux'
import {put, take} from 'redux-saga/effects'

import actions, {actionTypes} from '../actions'
import Fetching from '../components/Fetching'
import {store} from '../main'

const PASSWORD_FORM_MANUAL = 'manual'
const PASSWORD_FORM_GENERATED = 'generated'


/**
 * User情報の確認、編集
 */
class User extends React.Component {
  static propTypes = {
    isFetching: PropTypes.bool.isRequired,
    // isDeleteAsking: PropTypes.bool.isRequired,
    users: PropTypes.object.isRequired,
    actions: PropTypes.object.isRequired,
  }

  /**
   * @constructor
   */
  constructor(...args) {
    super(...args)

    this.state = {
      passwordForm: PASSWORD_FORM_MANUAL,   // 'manual' or 'generated'
      generatedPassword: null,
      openPasswordCopiedSnackbar: false,
      openUpdatedSnackbar: false,
      errors: {},
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

    return this.renderUserForm(user)
  }

  /**
   * ユーザー情報フォームを描画する
   * @param {User} user ユーザー
   * @return {React.Component}
   */
  renderUserForm(user) {
    const title = `ユーザー ${user.displayName}`
    const {
      errors,
    } = this.state

    return (
      <div className="metadataForm">
        <Title render={(previousTitle) => `${title} - ${previousTitle}`} />

        <div className="markdown-body">
          <h2>{title}</h2>
        </div>

        <form ref="form" onSubmit={::this.onSubmitForm}>
          <TextField
            name="account"
            hintText="userA"
            floatingLabelText="アカウント"
            floatingLabelFixed={true}
            defaultValue={user.account}
            errorText={errors.account}
          /><br />

          <TextField
            name="work"
            hintText="◯◯大学"
            floatingLabelText="所属"
            floatingLabelFixed={true}
            defaultValue={user.work}
            errorText={errors.work}
          /><br />

          <TextField
            name="mailAddress"
            hintText="user@example.com"
            floatingLabelText="メールアドレス"
            floatingLabelFixed={true}
            defaultValue={user.mailAddress}
            errorText={errors.mailAddress}
          /><br />

          <TextField
            name="telephone"
            hintText="0X0-XXXX-XXXX"
            floatingLabelText="電話番号"
            floatingLabelFixed={true}
            defaultValue={user.telephone}
            errorText={errors.telephone}
          /><br />

          <div style={{margin: '2rem 0'}}>
            <Checkbox name="isAdmin" label="管理者" defaultChecked={user.isAdmin} />
            {errors.permission && <p>{errors.permissions}</p>}
          </div>

          {this.state.passwordForm === PASSWORD_FORM_MANUAL
            ? this.renderManualPasswordForm()
            : this.renderGeneratedPasswordForm()}

          <div className="metadataForm-actions">
            <RaisedButton
              label="保存する"
              primary={true}
              onTouchTap={::this.onTapSave}
            />
          </div>
        </form>

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
   * パスワード手動設定フォームを描画する
   * @return {React.Component}
   */
  renderManualPasswordForm() {
    const {
      errors,
    } = this.state

    return (
      <div>
        <TextField
          name="currentPassword"
          hintText="現在のパスワード"
          floatingLabelText="現在のパスワード"
          floatingLabelFixed={true}
          type="password"
          errorText={errors.currentPassword}
        /><br />

        <TextField
          name="newPassword"
          hintText="新しいパスワード"
          floatingLabelText="新しいパスワード"
          floatingLabelFixed={true}
          type="password"
          errorText={errors.newPassword}
        /><br />

        <TextField
          name="newPasswordRe"
          hintText="新しいパスワードを確認"
          floatingLabelText="新しいパスワードを確認"
          floatingLabelFixed={true}
          type="password"
          errorText={errors.newPasswordRe}
        /><br />

        <FlatButton
          label="新しいパスワードを自動生成する"
          onTouchTap={::this.onTapGeneratePassword} />
      </div>
    )
  }

  /**
   * パスワード自動設定フォームを描画する
   * @return {React.Component}
   */
  renderGeneratedPasswordForm() {
    const {
      errors,
    } = this.state

    return (
      <div>
        <TextField
          name="currentPassword"
          hintText="現在のパスワード"
          floatingLabelText="現在のパスワード"
          floatingLabelFixed={true}
          type="password"
          errorText={errors.currentPassword}
        /><br />

        <TextField
          ref="generatedPassword"
          name="newPassword"
          floatingLabelText="パスワード"
          floatingLabelFixed={true}
          readOnly={true}
          value={this.state.generatedPassword}
          onChange={() => {}}
          errorText={errors.newPassword}
        />
        <IconButton tooltip="パスワードをクリップボードにコピー" onTouchTap={::this.onTapCopyGeneratedPassword}>
          <FontIcon className="material-icons">input</FontIcon>
        </IconButton>
        <br />

        <FlatButton
          label="新しいパスワードを自分で決める"
          onTouchTap={::this.onTapManualPassword} />

        <Snackbar
          open={this.state.openPasswordCopiedSnackbar}
          message="パスワードをクリップボードにコピーしました。"
          autoHideDuration={2000}
          onRequestClose={() => this.setState({openPasswordCopiedSnackbar: false})}
        />
      </div>
    )
  }

  /**
   * パスワード自動生成が押されたら呼ばれる。自動生成フォームを表示する
   */
  onTapGeneratePassword() {
    let generatedPassword = makePassword()
    this.setState({passwordForm: PASSWORD_FORM_GENERATED, generatedPassword})
  }

  /**
   * パスワード手動設定が押されたら呼ばれる。手動設定フォームを表示する
   */
  onTapManualPassword() {
    this.setState({passwordForm: PASSWORD_FORM_MANUAL, generatedPassword: null})
  }

  /**
   * 自動生成パスワードのコピーボタンが押されたら呼ばれる
   */
  onTapCopyGeneratedPassword() {
    const r = document.createRange()
    r.selectNode(this.refs.generatedPassword.input)
    window.getSelection().addRange(r)
    document.execCommand('copy')

    this.setState({openPasswordCopiedSnackbar: true})
  }

  /**
   * 保存ボタンが押されたら呼ばれる。保存する
   * @param {Event} e event object
   */
  onTapSave(e) {
    e.preventDefault()
    this.submitFormData()
  }

  /**
   * FormのonSubmitでも呼ばれるので保存する
   * @param {Event} e event object
   */
  onSubmitForm(e) {
    // XHRで処理するので
    e.preventDefault()
    this.submitFormData()
  }

  /**
   * User情報をサーバに保存する
   * @param {Event} e event object
   */
  submitFormData() {
    const user = this.props.users.get(this.props.params.userId)

    let params = {}
    const formData = new FormData(this.refs.form)
    for(let [key, val] of formData.entries()) {
      params[key] = val
    }

    // validation
    // TODO(値のvalidationはModel的なところでやる)
    let errors = {}

    if(!params.account)
      errors['account'] = 'アカウントは必須です'

    if(this.state.passwordForm === PASSWORD_FORM_GENERATED) {
      params.newPassword = this.state.generatedPassword
    }

    if(params.newPassword || params.newPasswordRe) {
      // 新しいパスワードを入れようとしている？
      if(!params.currentPassword)
        errors['currentPassword'] = '現在のパスワードを入力して下さい'
      if(!params.newPassword)
        errors['newPassword'] = '新しいパスワードを入力して下さい'
      if(this.state.passwordForm === PASSWORD_FORM_MANUAL && params.newPassword !== params.newPasswordRe)
        errors['newPasswordRe'] = '2つのパスワードが異なります'
    } else {
      // 新しいパスワードは無い
      if(params.currentPassword) {
        errors['newPassword'] = '新しいパスワードを入力して下さい'
      } else {
        delete params.currentPassword
        delete params.newPassword
        delete params.newPasswordRe
      }
    }

    if(params.isAdmin) {
      params.permissions = ['admin']
      delete params.isAdmin
    } else {
      params.permissions = []
    }


    if(Object.keys(errors).length) {
      this.setState({errors})
      return
    }

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
 * 16文字のランダムなパスワードとして使える文字列を生成する
 * @return {str} 自動生成されたパスワード文字列
 */
function makePassword() {
  const l = 16
  const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
  let r = ''

  for(let i = 0; i < l; i++) {
    r += chars[Math.floor(Math.random() * chars.length)]
  }
  return r
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
)(User)
