import React, {Component, PropTypes} from 'react'

import Checkbox from 'material-ui/Checkbox'
import TextField from 'material-ui/TextField'

import DisplayNameTextField from 'src/components/commons/DisplayNameTextField'
import WorkTextField from 'src/components/commons/WorkTextField'


/**
* UserInfo編集コンポーネント
*/
class UserInfoEditComponent extends Component {
  static propTypes = {
    user: PropTypes.object.isRequired,
    errors: PropTypes.object,
    onUpdate: PropTypes.func,
    canChangePermission: PropTypes.bool,
  }

  static defaultProps = {
    canChangePermission: true,
  }

  /**
   * @override
   */
  render() {
    const {
      canChangePermission,
      user,
      errors = {},
      onUpdate,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
        width: '100%',
      },
    }

    const accountErrorText = errors.account

    return (
      <div style={style.root}>
        <DisplayNameTextField
          obj={user}
          floatingLabelText="アカウント"
          errorText={accountErrorText}
          onChange={(e) => onUpdate(user.updateDisplayName(e.target.value))}
        />

        <Checkbox
          label="管理権限"
          disabled={!canChangePermission}
          style={{margin: '12px 0'}}
          checked={user.isAdmin}
          onCheck={(e, v) => onUpdate(user.updateIsAdmin(v))}
        />

        <WorkTextField
          obj={user}
          onChange={(e) => onUpdate(user.updateWork(e.target.value))}
        />
        <TextField
          floatingLabelText="メールアドレス"
          fullWidth={true}
          value={user.mailAddress}
          onChange={(e) => onUpdate(user.updateMailAddress(e.target.value))}
        />
        <TextField
          floatingLabelText="電話番号"
          fullWidth={true}
          value={user.telephone}
          onChange={(e) => onUpdate(user.updateTelephone(e.target.value))}
        />
      </div>
    )
  }
}


export default UserInfoEditComponent
