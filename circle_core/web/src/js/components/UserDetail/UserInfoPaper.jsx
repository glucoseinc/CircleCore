import PropTypes from 'prop-types'
import React from 'react'

import Paper from 'material-ui/Paper'

import LabelWithCopyButton from 'src/containers/bases/LabelWithCopyButton'
import ComponentWithSubTitle from 'src/components/bases/ComponentWithSubTitle'
import {EmailIcon, PhoneIcon, WorkIcon} from 'src/components/bases/icons'
import CCRaisedButton from 'src/components/bases/CCRaisedButton'

/**
* UserInfoコンポーネント
*/
class UserInfoPaper extends React.Component {
  static propTypes = {
    isMe: PropTypes.bool.isRequired,
    user: PropTypes.object.isRequired,
    onRenewTokenRequested: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      isMe,
      user,
      onRenewTokenRequested,
    } = this.props

    const styles = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
        padding: 24,
      },
      label: {
        fontSize: 14,
        lineHeight: 1.1,
      },

      workArea: {
      },

      mailAdressArea: {
        paddingTop: 16,
      },

      telephoneArea: {
        paddingTop: 16,
      },

      tokenArea: {
        paddingTop: 16,
      },

      tokenLabel: {
        display: 'flex',
        alignItems: 'center',
      },
      token: {
        flex: 'auto',
        fontSize: 14,
        lineHeight: 1.1,
      },
      renewButton: {
        marginLeft: '8px',
        minWidth: '120px',
      },
    }

    return (
      <Paper>
        <div style={styles.root}>
          <div style={styles.workArea}>
            <ComponentWithSubTitle subTitle="所属" icon={WorkIcon}>
              <div style={styles.label}>
                {user.work || '(未入力)'}
              </div>
            </ComponentWithSubTitle>
          </div>

          <div style={styles.mailAdressArea}>
            <ComponentWithSubTitle subTitle="メールアドレス" icon={EmailIcon}>
              <div style={styles.label}>
                {user.mailAddress || '(未入力)'}
              </div>
            </ComponentWithSubTitle>
          </div>

          <div style={styles.telephoneArea}>
            <ComponentWithSubTitle subTitle="電話番号" icon={PhoneIcon}>
              <div style={styles.label}>
                {user.telephone || '(未入力)'}
              </div>
            </ComponentWithSubTitle>
          </div>

          {isMe &&
            <div style={styles.tokenArea}>
              <ComponentWithSubTitle subTitle="トークン" icon={PhoneIcon}>
                <div style={styles.tokenLabel}>
                  {user.token ?
                    <LabelWithCopyButton
                      label={user.token}
                      style={styles.token}
                      messageWhenCopying="トークンをコピーしました"
                    /> :
                    <div style={styles.token}>トークンはありません</div>
                  }
                  <CCRaisedButton
                    style={styles.renewButton}
                    label={user.token ? '再生成する' : '生成する'} onClick={() => onRenewTokenRequested(user)}
                  />
                </div>
              </ComponentWithSubTitle>
            </div>
          }
        </div>
      </Paper>
    )
  }
}


export default UserInfoPaper
