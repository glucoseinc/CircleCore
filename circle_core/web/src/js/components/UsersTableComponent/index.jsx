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
    onDisplayNameClick: PropTypes.func,
    onDeleteClick: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      users,
      myID = null,
      readOnly = true,
      onDisplayNameClick,
      onDeleteClick,
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
                onDisplayNameClick={onDisplayNameClick}
                onDeleteClick={onDeleteClick}
              />
            ))}
          </div>
        </div>
      </div>
    )
  }
}


export default UsersTableComponent
