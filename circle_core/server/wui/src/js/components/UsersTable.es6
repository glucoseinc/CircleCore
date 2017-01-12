import React, {PropTypes} from 'react'

// import FlatButton from 'material-ui/FlatButton'
// import RaisedButton from 'material-ui/RaisedButton'
import Checkbox from 'material-ui/Checkbox'
import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn} from 'material-ui/Table'
import {colorUUID} from '../colors'

import CCLink from '../components/CCLink'
import {urls} from '../routes'
import User from '../models/User'


/**
 * ユーザー一覧の各行
 */
class UsersTableRow extends React.Component {
  static propTypes = {
    user: PropTypes.instanceOf(User).isRequired,
  }

  /**
   * @override
   */
  render() {
    const {user} = this.props
    const style = {
      subtext: {
        color: colorUUID,
        fontSize: 10,
      },
    }

    return (
      <TableRow>
        <TableRowColumn>
          <CCLink
            url={urls.user}
            params={{userId: user.uuid}}
          >
            {user.displayName}<br/>
            <span style={style.subtext}>{user.uuid}</span>
          </CCLink>
        </TableRowColumn>
        <TableRowColumn>{user.mailAddress}</TableRowColumn>
        <TableRowColumn><Checkbox label="" checked={user.isAdmin} disabled={true} /></TableRowColumn>
      </TableRow>
    )
  }
}


/**
 */
export default class UsersTable extends React.Component {
  static propTypes = {
    users: PropTypes.array.isRequired,
    onDeleteTouchTap: PropTypes.func.isRequired,
  }

  static contextTypes = {
    muiTheme: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      users,
      // onDeleteTouchTap,
    } = this.props

    return (
      <Table>
        <TableHeader
          displaySelectAll={false}
          adjustForCheckbox={false}
        >
          <TableRow>
            <TableHeaderColumn tooltip="User account">アカウント</TableHeaderColumn>
            <TableHeaderColumn tooltip="メールアドレス">メールアドレス</TableHeaderColumn>
            <TableHeaderColumn tooltip="管理者であればチェック">管理者</TableHeaderColumn>
          </TableRow>
        </TableHeader>

        <TableBody
          displayRowCheckbox={false}
        >
          {users.map((user) => <UsersTableRow key={user.uuid} user={user} />)}
        </TableBody>
      </Table>
    )
  }
}
