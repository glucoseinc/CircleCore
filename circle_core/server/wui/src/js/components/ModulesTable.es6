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
    modules: PropTypes.array.isRequired,
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
    const {
      muiTheme,
    } = this.context

    const style = {
      messageBoxButton: {
        maxWidth: muiTheme.button.minWidth + 32,
      },
      chip: {
        display: 'inline-flex',
        margin: 2,
      },
      subtext: {
        color: blueGrey600,
        fontSize: 10,
      },
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
          {modules.map((module) =>
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
                {module.metadata.tags.map((tag) =>
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
