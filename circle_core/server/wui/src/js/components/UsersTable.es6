import React, {PropTypes} from 'react'

// import FlatButton from 'material-ui/FlatButton'
// import RaisedButton from 'material-ui/RaisedButton'
import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn} from 'material-ui/Table'
import {colorUUID} from '../colors'

import CCLink from '../components/CCLink'
import {urls} from '../routes'


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
    const {
      muiTheme,
    } = this.context

    const style = {
      moduleButton: {
        maxWidth: muiTheme.button.minWidth + 32,
      },
      subtext: {
        color: colorUUID,
        fontSize: 10,
      },
    }

    return (
      <Table>
        <TableHeader
          displaySelectAll={false}
          adjustForCheckbox={false}
        >
          <TableRow>
            <TableHeaderColumn tooltip="User account">Name</TableHeaderColumn>
            <TableHeaderColumn tooltip="Modules using schema">Modules</TableHeaderColumn>
            <TableHeaderColumn></TableHeaderColumn>
          </TableRow>
        </TableHeader>

        <TableBody
          displayRowCheckbox={false}
        >
          {users.map((user) =>
            <TableRow key={users.uuid}>
              <TableRowColumn>
                <CCLink
                  url={urls.users}
                  params={{schemaId: users.uuid}}
                >
                  {user.displayName}<br/>
                  <span style={style.subtext}>{user.uuid}</span>
                </CCLink>
              </TableRowColumn>
            </TableRow>
          )}
        </TableBody>
      </Table>
    )
  }
}
