import React, {Component, PropTypes} from 'react'

import UserInfoPaper from './UserInfoPaper'
import UsersHeader from './UsersHeader'


/**
* Userテーブルコンポーネント
*/
class UsersTableComponent extends Component {
  static propTypes = {
    users: PropTypes.object.isRequired,
    readOnly: PropTypes.bool,
    onDisplayNameTouchTap: PropTypes.func,
    onDeleteTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      users,
      readOnly = true,
      onDisplayNameTouchTap,
      onDeleteTouchTap,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
      },
    }

    return (
      <div style={style.root}>
        <div>
          <div style={style.header}>
            <UsersHeader />
          </div>
          <div style={style.row}>
            {users.valueSeq().map((user, index) =>
              <UserInfoPaper
                key={user.uuid}
                user={user}
                readOnly={readOnly}
                onDisplayNameTouchTap={onDisplayNameTouchTap}
                onDeleteTouchTap={onDeleteTouchTap}
              />
            )}
          </div>
        </div>
      </div>
    )
  }
}


export default UsersTableComponent
