import React, {Component} from 'react'

import {grey600} from 'material-ui/styles/colors'

import tableStyle from './tableStyle'


/**
* UsersHeader
*/
class UsersHeader extends Component {
  static propTypes = {
  }

  /**
   * @override
   */
  render() {
    const style = {
      root: {
        ...tableStyle.root,
        fontSize: 12,
        color: grey600,
      },
      displayName: {
        ...tableStyle.displayName,
      },
      mailAddress: {
        ...tableStyle.mailAddress,
      },
      dateLastAccess: {
        ...tableStyle.dateLastAccess,
      },
      isAdmin: {
        ...tableStyle.isAdmin,
      },
    }

    return (
      <div style={style.root}>
        <div style={style.displayName}>アカウント</div>
        <div style={style.mailAddress}>メールアドレス</div>
        <div style={style.dateLastAccess}>最終ログイン日時</div>
        <div style={style.isAdmin}>管理権限</div>
      </div>
    )
  }
}


export default UsersHeader
