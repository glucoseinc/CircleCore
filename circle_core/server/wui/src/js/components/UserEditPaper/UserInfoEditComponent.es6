import React, {Component, PropTypes} from 'react'

import TextField from 'material-ui/TextField'

import DisplayNameTextField from 'src/components/commons/DisplayNameTextField'
import WorkTextField from 'src/components/commons/WorkTextField'


/**
* UserInfo編集コンポーネント
*/
class UserInfoEditComponent extends Component {
  static propTypes = {
    user: PropTypes.object.isRequired,
    onUpdate: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      user,
      onUpdate,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
        width: '100%',
      },
    }

    return (
      <div style={style.root}>
        <DisplayNameTextField
          obj={user}
          floatingLabelText="アカウント"
          onChange={(e) => onUpdate(user.updateDisplayName(e.target.value))}
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
