import React, {Component, PropTypes} from 'react'

import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn} from 'material-ui/Table'

import {colorUUID} from 'src/colors'
import Invitation from 'src/models/Invitation'

import DeleteButton from 'src/components/commons/DeleteButton'


const styles = {
  subtext: {
    color: colorUUID,
    fontSize: 10,
  },
  columnInvites: {
    width: '4em',
  },
}

/**
 * 招待一覧の各行
 */
class InvitationsTableRow extends Component {
  static propTypes = {
    invitation: PropTypes.instanceOf(Invitation).isRequired,
    onDeleteInvitation: PropTypes.func.isRequired,
    readOnly: PropTypes.bool,
  }

  static defaultProps = {
    readOnly: true,
  }

  /**
   * @override
   */
  render() {
    const {invitation} = this.props


    return (
      <TableRow>
        <TableRowColumn>
          <a target="_blank" href={invitation.url}>{invitation.url}</a><br />
          <span style={styles.subtext}>{invitation.uuid}</span>
        </TableRowColumn>
        <TableRowColumn style={styles.columnInvites}>
          {invitation.maxInvites == 0 ? '∞' : invitation.maxInvites - invitation.currentInvites}
        </TableRowColumn>
        <TableRowColumn>
          {invitation.dateCreated.format('LLL')}
        </TableRowColumn>
        <TableRowColumn>
          {!this.props.readOnly &&
          <DeleteButton
            onTouchTap={(e) => this.props.onDeleteInvitation(invitation, e)}
          />}
        </TableRowColumn>
      </TableRow>
    )
  }
}


/**
 * 招待一覧
 */
export default class InvitationsTable extends Component {
  static propTypes = {
    invitations: PropTypes.object.isRequired,
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
            <TableHeaderColumn tooltip="このリンクから作成できるユーザーの残り数" style={styles.columnInvites}>
              残招待数
            </TableHeaderColumn>
            <TableHeaderColumn tooltip="招待を作成した日">作成日</TableHeaderColumn>
            <TableHeaderColumn tooltip=""></TableHeaderColumn>
          </TableRow>
        </TableHeader>

        <TableBody
          displayRowCheckbox={false}
        >
          {invitations.valueSeq().sortBy((v) => v.dateCreated).reverse().map((invitation) =>
            <InvitationsTableRow
              key={invitation.uuid}
              invitation={invitation}
              onDeleteInvitation={onDeleteInvitation} />)}
        </TableBody>
      </Table>
    )
  }
}