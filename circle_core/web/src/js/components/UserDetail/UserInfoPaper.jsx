import PropTypes from 'prop-types'
import React from 'react'

import Paper from 'material-ui/Paper'

import ComponentWithSubTitle from 'src/components/bases/ComponentWithSubTitle'
import {EmailIcon, PhoneIcon, WorkIcon} from 'src/components/bases/icons'


/**
* UserInfoコンポーネント
*/
class UserInfoPaper extends React.Component {
  static propTypes = {
    user: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      user,
    } = this.props

    const style = {
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
    }

    return (
      <Paper>
        <div style={style.root}>
          <div style={style.workArea}>
            <ComponentWithSubTitle subTitle="所属" icon={WorkIcon}>
              <div style={style.label}>
                {user.work || '(未入力)'}
              </div>
            </ComponentWithSubTitle>
          </div>

          <div style={style.mailAdressArea}>
            <ComponentWithSubTitle subTitle="メールアドレス" icon={EmailIcon}>
              <div style={style.label}>
                {user.mailAddress || '(未入力)'}
              </div>
            </ComponentWithSubTitle>
          </div>

          <div style={style.telephoneArea}>
            <ComponentWithSubTitle subTitle="電話番号" icon={PhoneIcon}>
              <div style={style.label}>
                {user.telephone || '(未入力)'}
              </div>
            </ComponentWithSubTitle>
          </div>
        </div>
      </Paper>
    )
  }
}


export default UserInfoPaper
