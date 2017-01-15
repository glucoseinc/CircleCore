import React, {PropTypes} from 'react'

import RaisedButton from 'material-ui/RaisedButton'
import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn} from 'material-ui/Table'
import {colorUUID} from '../colors'

import Invitation from '../models/Invitation'


/**
 * 招待一覧の各行
 */
class InvitationsTableRow extends React.Component {
  static propTypes = {
    invitation: PropTypes.instanceOf(Invitation).isRequired,
    onDeleteInvitation: PropTypes.func.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {invitation} = this.props
    const style = {
      subtext: {
        color: colorUUID,
        fontSize: 10,
      },
    }

    return (
      <TableRow>
        <TableRowColumn>
          <a target="_blank" href={invitation.link}>{invitation.link}</a><br />
          <span style={style.subtext}>{invitation.uuid}</span>
        </TableRowColumn>
        <TableRowColumn>
          {invitation.maxInvites == 0 ? '∞' : invitation.maxInvites - invitation.currentInvites}
        </TableRowColumn>
        <TableRowColumn>
          <RaisedButton
            label="削除"
            secondary={true}
            onTouchTap={(e) => this.props.onDeleteInvitation(invitation, e)}
          />
        </TableRowColumn>
      </TableRow>
    )
  }
}


/**
 * 招待一覧
 */
export default class InvitationsTable extends React.Component {
  static propTypes = {
    invitations: PropTypes.array.isRequired,
    onDeleteInvitation: PropTypes.func.isRequired,
  }

  static contextTypes = {
    muiTheme: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      invitations,
      onDeleteInvitation,
    } = this.props

    return (
      <Table>
        <TableHeader
          displaySelectAll={false}
          adjustForCheckbox={false}
        >
          <TableRow>
            <TableHeaderColumn tooltip="招待ページのURL">リンク</TableHeaderColumn>
            <TableHeaderColumn tooltip="このリンクから作成できるユーザーの残り数">残招待数</TableHeaderColumn>
            <TableHeaderColumn tooltip=""></TableHeaderColumn>
          </TableRow>
        </TableHeader>

        <TableBody
          displayRowCheckbox={false}
        >
          {invitations.map((invitation) =>
            <InvitationsTableRow
              key={invitation.uuid}
              invitation={invitation}
              onDeleteInvitation={onDeleteInvitation} />)}
        </TableBody>
      </Table>
    )
  }
}
