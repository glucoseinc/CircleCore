import PropTypes from 'prop-types'
import React from 'react'

import Paper from 'material-ui/Paper'
import TextField from 'material-ui/TextField'

import ComponentWithHeader from 'src/components/bases/ComponentWithHeader'
import PasswordChangeComponent from 'src/components/commons/PasswordChangeComponent'
import SaveButton from 'src/components/commons/SaveButton'
import UserInfoEditComponent from './UserInfoEditComponent'


/**
* User編集
*/
class UserEditPaper extends React.Component {
  static propTypes = {
    user: PropTypes.object.isRequired,
    errors: PropTypes.object,
    needCurrentPassword: PropTypes.bool,
    onSaveClick: PropTypes.func,
    onRenewTokenRequested: PropTypes.func,
    saveButtonLabel: PropTypes.string, // パスワードの入力が必須かどうか?
    isPasswordRequired: PropTypes.bool,
    canChangePermission: PropTypes.bool,
    hideAdminCheck: PropTypes.bool,
    hideToken: PropTypes.bool,
  }

  static defaultProps = {
    isPasswordRequired: false,
    canChangePermission: true,
    hideAdminCheck: false,
    hideToken: false,
  }

  /**
   * @override
   */
  constructor(props) {
    super(props)
    this.state = {
      editingUser: this.props.user,
      currentPassword: '',
      newPassword: undefined,
    }
  }

  /**
   * @return {bool}
   */
  isReadyToSave() {
    if (!(this.state.editingUser.isReadytoCreate() && this.state.newPassword !== null)) {
      return false
    }

    if (this.props.isPasswordRequired && !this.state.newPassword) {
      return false
    }

    return true
  }

  /**
   * @override
   */
  render() {
    const {
      editingUser,
      currentPassword,
      newPassword,
    } = this.state
    const {
      user,
      needCurrentPassword = false,
      errors = {},
      hideAdminCheck,
      hideToken,
      onSaveClick,
      onRenewTokenRequested,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
        padding: 24,
      },

      userInfoArea: {
      },

      changePasswordArea: {
        paddingTop: 32,
      },

      actionsArea: {
        display: 'flex',
        flexFlow: 'row nowrap',
        justifyContent: 'space-around',
        paddingTop: 40,
      },
    }

    const currentPasswordErrorText = errors.currentPassword
    const currentPasswordTextField = needCurrentPassword ? (
      <TextField
        floatingLabelText="現在のパスワード"
        value={currentPassword}
        type="password"
        errorText={currentPasswordErrorText}
        onChange={(e) => this.setState({currentPassword: e.target.value})}
      />
    ) : (
      null
    )

    return (
      <Paper>
        <div style={style.root}>
          <div style={style.userInfoArea}>
            <ComponentWithHeader headerLabel="ユーザー情報">
              <UserInfoEditComponent
                source={user}
                current={editingUser}
                errors={errors}
                hideAdminCheck={hideAdminCheck}
                hideToken={hideToken}
                canChangePermission={this.props.canChangePermission}
                onUpdate={(user) => this.setState({editingUser: user})}
                onRenewTokenRequested={() => onRenewTokenRequested(editingUser)}
              />
            </ComponentWithHeader>
          </div>

          <div style={style.changePasswordArea}>
            <ComponentWithHeader headerLabel="パスワード">
              {currentPasswordTextField}
              <PasswordChangeComponent
                errors={errors}
                onUpdate={(newPassword) => this.setState({newPassword})}
              />
            </ComponentWithHeader>
          </div>

          <div style={style.actionsArea}>
            <SaveButton
              label={this.props.saveButtonLabel}
              disabled={this.isReadyToSave() ? false : true}
              onClick={() => onSaveClick(editingUser, currentPassword, newPassword)}
            />
          </div>
        </div>
      </Paper>
    )
  }
}


export default UserEditPaper
