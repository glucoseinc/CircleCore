import PropTypes from 'prop-types'
import React from 'react'

import ComponentWithTitle from 'src/components/bases/ComponentWithTitle'
import DisplayNamePaper from 'src/components/commons/DisplayNamePaper'

import UserInfoPaper from './UserInfoPaper'


/**
* User詳細コンポーネント
*/
class UserDetail extends React.Component {
  static propTypes = {
    user: PropTypes.object.isRequired,
    isMe: PropTypes.bool.isRequired,
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

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
      },

      displayNamePaper: {
      },

      infoArea: {
        paddingTop: 32,
      },

    }

    return (
      <div style={style.root}>
        <div style={style.displayNamePaper}>
          <DisplayNamePaper
            obj={user}
            secondaryType="id"
          />
        </div>

        <div style={style.infoArea}>
          <ComponentWithTitle title="ユーザー情報">
            <UserInfoPaper isMe={isMe} user={user} onRenewTokenRequested={onRenewTokenRequested} />
          </ComponentWithTitle>
        </div>
      </div>
    )
  }
}


export default UserDetail
