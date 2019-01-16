import PropTypes from 'prop-types'
import React from 'react'

import Checkbox from 'material-ui/Checkbox'
import TextField from 'material-ui/TextField'

import DisplayNameTextField from 'src/components/commons/DisplayNameTextField'
import WorkTextField from 'src/components/commons/WorkTextField'
import LabelWithCopyButton from 'src/containers/bases/LabelWithCopyButton'
import CCRaisedButton from 'src/components/bases/CCRaisedButton'


/**
 * UserInfo編集コンポーネント
 *
 * @param {props} props
 * @return {React.Compoonent}
 */
const UserInfoEditComponent = (props) => {
  const {
    canChangePermission,
    source,
    current,
    errors = {},
    hideAdminCheck,
    hideToken,
    onUpdate,
    onRenewTokenRequested,
  } = props

  const styles = {
    root: {
      display: 'flex',
      flexFlow: 'column nowrap',
      width: '100%',
    },

    tokenFormGroup: {
      marginTop: '1ex',
    },

    inputLabel: {
      fontSize: '0.75rem',
    },

    noToken: {
      color: 'rgba(0, 0, 0, 0.3)',
      flex: 'auto',
    },

    token: {
      flex: 'auto',
    },

    tokenRow: {
      display: 'flex',
    },

    renewButton: {
      marginLeft: '8px',
      minWidth: '120px',
    },
  }

  const accountErrorText = errors.account

  return (
    <div style={styles.root}>
      <DisplayNameTextField
        obj={current}
        floatingLabelText="アカウント"
        errorText={accountErrorText}
        onChange={(e) => onUpdate(current.updateDisplayName(e.target.value))}
      />
      {!hideAdminCheck &&
        <Checkbox
          label="管理権限"
          disabled={!canChangePermission}
          style={{margin: '12px 0'}}
          checked={current.isAdmin}
          onCheck={(e, v) => onUpdate(current.updateIsAdmin(v))}
        />
      }

      <WorkTextField
        obj={current}
        onChange={(e) => onUpdate(current.updateWork(e.target.value))}
      />
      <TextField
        floatingLabelText="メールアドレス"
        fullWidth={true}
        value={current.mailAddress}
        onChange={(e) => onUpdate(current.updateMailAddress(e.target.value))}
      />
      <TextField
        floatingLabelText="電話番号"
        fullWidth={true}
        value={current.telephone}
        onChange={(e) => onUpdate(current.updateTelephone(e.target.value))}
      />
      {!hideToken &&
        <div style={styles.tokenFormGroup}>
          <div style={styles.inputLabel}>トークン</div>
          <div style={styles.tokenRow}>
            {source.token ?
              <LabelWithCopyButton
                label={source.token}
                style={styles.token}
                messageWhenCopying="トークンをコピーしました"
              /> :
              <div style={styles.noToken}>トークンはありません</div>
            }
            <CCRaisedButton
              style={styles.renewButton}
              label={source.token ? '再生成する' : '生成する'} onClick={onRenewTokenRequested}
            />
          </div>
        </div>
      }
    </div>
  )
}
UserInfoEditComponent.propTypes = {
  canChangePermission: PropTypes.bool,
  source: PropTypes.object.isRequired,
  current: PropTypes.object.isRequired,
  errors: PropTypes.object,
  hideAdminCheck: PropTypes.bool,
  hideToken: PropTypes.bool,
  onUpdate: PropTypes.func,
  onRenewTokenRequested: PropTypes.func,
}
UserInfoEditComponent.defaultProps = {
  canChangePermission: true,
}

export default UserInfoEditComponent
