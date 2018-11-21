import PropTypes from 'prop-types'
import React from 'react'

import UserInfoPaper from './UserInfoPaper'
import UsersHeader from './UsersHeader'


/**
* Userテーブルコンポーネント
*/
class UsersTableComponent extends React.Component {
  static propTypes = {
    users: PropTypes.object.isRequired,
    myID: PropTypes.string,
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
      myID = null,
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
            {users.valueSeq().map((user, index) => (
              <UserInfoPaper
                key={user.uuid}
                user={user}
                deleteDisabled={myID === null || myID === user.uuid}
                readOnly={readOnly}
                onDisplayNameTouchTap={onDisplayNameTouchTap}
                onDeleteTouchTap={onDeleteTouchTap}
              />
            ))}
          </div>
        </div>
      </div>
    )
  }
}


export default UsersTableComponent
