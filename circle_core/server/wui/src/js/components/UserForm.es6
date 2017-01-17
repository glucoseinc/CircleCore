/**
 * ユーザー情報を表示したり編集したりするForm
 */
import {Checkbox, IconButton, FlatButton, FontIcon, TextField, RaisedButton, Snackbar} from 'material-ui'
import React, {PropTypes} from 'react'

const PASSWORD_FORM_MANUAL = 'manual'
const PASSWORD_FORM_GENERATED = 'generated'


/**
 * User情報の確認、編集
 */
export default class UserForm extends React.Component {
  static propTypes = {
    errors: PropTypes.object,
    readOnly: PropTypes.bool.isRequired,
    showCurrentPasswordFiled: PropTypes.bool,
    showPermissionFields: PropTypes.bool,
    user: PropTypes.object.isRequired,
  }
  static defaultProps = {
    errors: {},
    readOnly: true,
    showCurrentPasswordFiled: false,
    showPermissionFields: false,
  }

  /**
   * @constructor
   */
  constructor(...args) {
    super(...args)

    this.state = {
      errors: {},
      generatedPassword: null,
      openPasswordCopiedSnackbar: false,
      passwordForm: PASSWORD_FORM_MANUAL,   // 'manual' or 'generated'
    }
  }

  /**
   * @override
   */
  render() {
    const {
      user,
      readOnly,
    } = this.props

    const errors = Object.assign({}, this.state.errors, this.props.errors)

    return (
      <div className="metadataForm">
        <form ref="form" onSubmit={::this.onSubmitForm}>
          <TextField
            name="account"
            hintText="userA"
            floatingLabelText="アカウント"
            floatingLabelFixed={true}
            defaultValue={user.account}
            readOnly={readOnly}
            errorText={errors.account}
          /><br />

          <TextField
            name="work"
            hintText="◯◯大学"
            floatingLabelText="所属"
            floatingLabelFixed={true}
            defaultValue={user.work}
            readOnly={readOnly}
            errorText={errors.work}
          /><br />

          <TextField
            name="mailAddress"
            hintText="user@example.com"
            floatingLabelText="メールアドレス"
            floatingLabelFixed={true}
            defaultValue={user.mailAddress}
            readOnly={readOnly}
            errorText={errors.mailAddress}
          /><br />

          <TextField
            name="telephone"
            hintText="0X0-XXXX-XXXX"
            floatingLabelText="電話番号"
            floatingLabelFixed={true}
            defaultValue={user.telephone}
            readOnly={readOnly}
            errorText={errors.telephone}
          /><br />

          {this.props.showPermissionFields &&
          <div style={{margin: '2rem 0'}}>
            <Checkbox name="isAdmin" label="管理者" defaultChecked={user.isAdmin} disabled={readOnly} />
            {errors.permission && <p>{errors.permissions}</p>}
          </div>}

          {!readOnly && this.renderPasswordForm(errors)}

          {!readOnly &&
          <div className="metadataForm-actions">
            <RaisedButton
              label="保存する"
              primary={true}
              onTouchTap={::this.onTapSave}
            />
          </div>}
        </form>
      </div>
    )
  }

  /**
   * パスワード設定フォームを描画する
   * @param {Object} errors
   * @return {React.Component}
   */
  renderPasswordForm(errors) {
    return (
      <div>
        {this.props.showCurrentPasswordFiled &&
          <div>
            <TextField
              name="currentPassword"
              hintText="現在のパスワード"
              floatingLabelText="現在のパスワード"
              floatingLabelFixed={true}
              type="password"
              errorText={errors.currentPassword}
            /><br />
          </div>}

        {this.state.passwordForm === PASSWORD_FORM_MANUAL
          ? this.renderManualPasswordForm(errors)
          : this.renderGeneratedPasswordForm(errors)}
      </div>
    )
  }

  /**
   * パスワード手動設定フォームを描画する
   * @param {Object} errors
   * @return {React.Component}
   */
  renderManualPasswordForm(errors) {
    return (
      <div>
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
   * @param {Object} errors
   * @return {React.Component}
   */
  renderGeneratedPasswordForm(errors) {
    return (
      <div>
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
    const node = this.refs.generatedPassword.input
    node.focus()
    node.setSelectionRange(0, node.value.length)
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
    let params = {}
    const formData = new FormData(this.refs.form)
    for(let [key, val] of formData.entries()) {
      params[key] = val
    }

    if(this.state.passwordForm === PASSWORD_FORM_GENERATED) {
      params.newPassword = params.newPasswordRe = this.state.generatedPassword
    }

    if(!params.newPassword && !params.newPasswordRe && !params.currentPassword) {
      delete params.currentPassword
      delete params.newPassword
      delete params.newPasswordRe
    }

    // errorチェック
    let errors = {}

    if(!params.account)
      errors['account'] = 'アカウントは必須です'

    if(params.newPassword || params.newPasswordRe) {
      // 新しいパスワードを入れようとしている？
      if(this.props.showCurrentPasswordFiled && !params.currentPassword)
        errors['currentPassword'] = '現在のパスワードを入力して下さい'
      if(!params.newPassword)
        errors['newPassword'] = '新しいパスワードを入力して下さい'
      if(params.newPassword !== params.newPasswordRe)
        errors['newPasswordRe'] = '2つのパスワードが異なります'
    } else {
      // 新しいパスワードは無い
      if(this.props.showCurrentPasswordFiled && params.currentPassword) {
        errors['newPassword'] = '新しいパスワードを入力して下さい'
      } else {
        delete params.currentPassword
        delete params.newPassword
        delete params.newPasswordRe
      }
    }

    if(this.props.showPermissionFields) {
      let permissions = []

      if(params.isAdmin) {
        permissions.push('admin')
      }
      params.permissions = []
    }

    //
    this.setState({errors})

    //  エラーがあればSubmitしない
    if(Object.keys(errors).length) {
      return
    }

    this.props.onSubmitUserForm(params)
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
