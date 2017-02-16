import React, {Component, PropTypes} from 'react'

import TextField from 'material-ui/TextField'

import CCFlatButton from 'src/components/bases/CCFlatButton'


/**
* パスワード手動変更コンポーネント
*/
class PasswordManualChangeComponent extends Component {
  static propTypes = {
    errors: PropTypes.object,
    onUpdate: PropTypes.func,
    onToggleInputMethod: PropTypes.func,
  }

  state = {
    password: '',
    confirmationPassword: '',
  }

  /**
   * 入力時の動作
   * @param {string} password
   * @param {string} confirmationPassword
   */
  onUpdate(password, confirmationPassword) {
    const newPassword = (password === '' && confirmationPassword === '') ? undefined :
      password === confirmationPassword ? password : null
    this.props.onUpdate(newPassword)
  }

  /**
   * @override
   */
  componentDidMount() {
    this.onUpdate('', '')
  }

  /**
   * パスワード欄変更時の動作
   * @param {string} value
   */
  onPasswordChange(value) {
    this.setState({password: value})
    this.onUpdate(value, this.state.confirmationPassword)
  }

  /**
   * 確認用パスワード欄変更時の動作
   * @param {string} value
   */
  onConfirmationPasswordChange(value) {
    this.setState({confirmationPassword: value})
    this.onUpdate(this.state.password, value)
  }

  /**
   * @override
   */
  render() {
    const {
      password,
      confirmationPassword,
    } = this.state
    const {
      errors = {},
      onToggleInputMethod,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
        alignItems: 'flex-start',
      },

      inputArea: {
        display: 'flex',
        flexFlow: 'column nowrap',
      },

      actionsArea: {
        paddingTop: 16,
      },
    }

    const newPasswordErrorText = errors.newPassword

    return (
      <div style={style.root}>
        <div style={style.inputArea}>
          <TextField
            floatingLabelText="新しいパスワード"
            value={password}
            type="password"
            errorText={newPasswordErrorText}
            onChange={(e) => this.onPasswordChange(e.target.value)}
          />
          <TextField
            floatingLabelText="新しいパスワード確認"
            value={confirmationPassword}
            type="password"
            errorText={
              (confirmationPassword.length && password !== confirmationPassword) ? 'パスワードが一致しません' : null
            }
            onChange={(e) => this.onConfirmationPasswordChange(e.target.value)}
          />
        </div>

        <div style={style.actionsArea}>
          <CCFlatButton
            label="新しいパスワードを自動生成する"
            primary={true}
            onTouchTap={onToggleInputMethod}
          />
        </div>
      </div>
    )
  }
}


export default PasswordManualChangeComponent
