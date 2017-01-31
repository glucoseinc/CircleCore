import React, {Component, PropTypes} from 'react'

import Checkbox from 'material-ui/Checkbox'
import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn} from 'material-ui/Table'

import {colorUUID} from 'src/colors'
import User from 'src/models/User'
import {urls} from 'src/routes'

import CCLink from 'src/components/commons/CCLink'
import DeleteButton from 'src/components/commons/DeleteButton'


/**
 * ユーザー一覧の各行
 */
class UsersTableRow extends Component {
  static propTypes = {
    user: PropTypes.instanceOf(User).isRequired,
    onDeleteUser: PropTypes.func.isRequired,
    readOnly: PropTypes.bool,
  }

  static defaultProps = {
    readOnly: true,
  }

  /**
   * @override
   */
  render() {
    const {
      user,
      readOnly,
    } = this.props
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
        <TableRowColumn>{user.dateLastAccess.format('LLL')}</TableRowColumn>
        <TableRowColumn>
          {!readOnly &&
          <DeleteButton
            onTouchTap={(e) => this.props.onDeleteUser(user, e)}
          />}
        </TableRowColumn>
      </TableRow>
    )
  }
}


/**
 */
export default class UsersTable extends Component {
  static propTypes = {
    users: PropTypes.object.isRequired,
    onDeleteUser: PropTypes.func.isRequired,
    readOnly: PropTypes.bool,
  }

  static contextTypes = {
    muiTheme: PropTypes.object.isRequired,
  }

  static defaultProps = {
    readOnly: 4,
  }

  /**
   * @override
   */
  render() {
    const {
      users,
      onDeleteUser,
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
            <TableHeaderColumn tooltip="ユーザが最後にアクセスした時刻">最終ログイン</TableHeaderColumn>
            <TableHeaderColumn></TableHeaderColumn>
          </TableRow>
        </TableHeader>

        <TableBody
          displayRowCheckbox={false}
        >
          {users.valueSeq().sortBy((v) => v.dateCreated).map((user) =>
            <UsersTableRow key={user.uuid} user={user} onDeleteUser={onDeleteUser} readOnly={this.props.readOnly} />
          )}
        </TableBody>
      </Table>
    )
  }
}
