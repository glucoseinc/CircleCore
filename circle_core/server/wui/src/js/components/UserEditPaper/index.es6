import React, {Component, PropTypes} from 'react'

import Paper from 'material-ui/Paper'
import TextField from 'material-ui/TextField'

import ComponentWithHeader from 'src/components/bases/ComponentWithHeader'
import PasswordChangeComponent from 'src/components/commons/PasswordChangeComponent'
import SaveButton from 'src/components/commons/SaveButton'
import UserInfoEditComponent from './UserInfoEditComponent'


/**
* User編集
*/
class UserEditPaper extends Component {
  static propTypes = {
    user: PropTypes.object.isRequired,
    needCurrentPassword: PropTypes.bool,
    onSaveTouchTap: PropTypes.func,
    saveButtonLabel: PropTypes.string,
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
    return this.state.editingUser.isReadytoCreate() && this.state.newPassword !== null
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
      needCurrentPassword = false,
      onSaveTouchTap,
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

    const currentPasswordTextField = needCurrentPassword ? (
      <TextField
        floatingLabelText="現在のパスワード"
        value={currentPassword}
        type="password"
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
                user={editingUser}
                onUpdate={(user) => this.setState({editingUser: user})}
              />
            </ComponentWithHeader>
          </div>

          <div style={style.changePasswordArea}>
            <ComponentWithHeader headerLabel="パスワード">
              {currentPasswordTextField}
              <PasswordChangeComponent
                onUpdate={(newPassword) => this.setState({newPassword})}
              />
            </ComponentWithHeader>
          </div>

          <div style={style.actionsArea}>
            <SaveButton
              label={this.props.saveButtonLabel}
              disabled={this.isReadyToSave() ? false : true}
              onTouchTap={() => onSaveTouchTap(editingUser, currentPassword, newPassword)}
            />
          </div>
        </div>
      </Paper>
    )
  }
}


export default UserEditPaper
