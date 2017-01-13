import React, {Component, PropTypes} from 'react'

import Chip from 'material-ui/Chip'
import RaisedButton from 'material-ui/RaisedButton'
import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn} from 'material-ui/Table'
import {blueGrey600} from 'material-ui/styles/colors'

import CCLink from '../components/CCLink'
import {urls} from '../routes'


/**
 */
class ModulesTable extends Component {
  static propTypes = {
    modules: PropTypes.object.isRequired,
    onTagTouchTap: PropTypes.func,
    onDeleteTouchTap: PropTypes.func,
  }

  static contextTypes = {
    muiTheme: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      modules,
      onTagTouchTap,
      onDeleteTouchTap,
    } = this.props

    const style = {
      chip: {
        display: 'inline-flex',
        margin: 2,
      },
      subtext: {
        color: blueGrey600,
        fontSize: 10,
      },
    }

    const sortComparator = (a, b) => {
      if (a.displayName !== '' && b.displayName === '') {
        return -1
      }
      if (a.displayName === '' && b.displayName !== '') {
        return 1
      }
      if (a.displayName !== '' && b.displayName !== '') {
        return a.displayName < b.displayName ? -1 : 1
      }
      return a.uuid < b.uuid ? -1 : 1
    }

    return (
      <Table
        selectable={false}
      >
        <TableHeader
          displaySelectAll={false}
          adjustForCheckbox={false}
        >
          <TableRow>
            <TableHeaderColumn tooltip="Module name">Name</TableHeaderColumn>
            <TableHeaderColumn tooltip="Attached message boxes">Message boxes</TableHeaderColumn>
            <TableHeaderColumn tooltip="Tags name">Tags</TableHeaderColumn>
            <TableHeaderColumn></TableHeaderColumn>
          </TableRow>
        </TableHeader>

        <TableBody
          displayRowCheckbox={false}
        >
          {modules.sort(sortComparator).valueSeq().map((module) =>
            <TableRow key={module.uuid}>
              <TableRowColumn>
                <CCLink
                  url={urls.module}
                  params={{moduleId: module.uuid}}
                >
                  {module.displayName}<br />
                  <span style={style.subtext}>{module.uuid}</span>
                </CCLink>
              </TableRowColumn>
              <TableRowColumn>
                {module.messageBoxes.map((messageBox) =>
                  <Chip
                    key={messageBox.uuid}
                    style={style.chip}
                  >
                    {messageBox.label}
                  </Chip>
                )}
              </TableRowColumn>
              <TableRowColumn>
                {module.tags.map((tag) =>
                  <Chip
                    style={style.chip}
                    key={tag}
                    onTouchTap={() => onTagTouchTap(tag)}
                  >
                    {tag}
                  </Chip>
                )}
              </TableRowColumn>
              <TableRowColumn>
                <RaisedButton
                  label="Delete"
                  secondary={true}
                  onTouchTap={() => onDeleteTouchTap(module)}
                />
              </TableRowColumn>
            </TableRow>
          )}
        </TableBody>
      </Table>
    )
  }
}

export default ModulesTable
