import React, {Component, PropTypes} from 'react'

import FlatButton from 'material-ui/FlatButton'
import RaisedButton from 'material-ui/RaisedButton'
import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn} from 'material-ui/Table'
import {blueGrey600} from 'material-ui/styles/colors'

import CCLink from '../components/CCLink'
import {urls} from '../routes'

/**
 */
class SchemasTable extends Component {
  static propTypes = {
    schemas: PropTypes.array.isRequired,
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
      schemas,
      onDeleteTouchTap,
    } = this.props
    const {
      muiTheme,
    } = this.context

    const style = {
      moduleButton: {
        maxWidth: muiTheme.button.minWidth + 32,
      },
      subtext: {
        color: blueGrey600,
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
            <TableHeaderColumn tooltip="Schema's name">Name</TableHeaderColumn>
            <TableHeaderColumn tooltip="Modules using schema">Modules</TableHeaderColumn>
            <TableHeaderColumn></TableHeaderColumn>
          </TableRow>
        </TableHeader>

        <TableBody
          displayRowCheckbox={false}
        >
          {schemas.map((schema) => {
            return (
              <TableRow key={schema.uuid}>
                <TableRowColumn>
                  <CCLink
                    url={urls.schema}
                    params={{schemaId: schema.uuid}}
                  >
                    {schema.display_name}<br/>
                    <span style={style.subtext}>{schema.uuid}</span>
                  </CCLink>
                </TableRowColumn>
                <TableRowColumn>
                  {schema.modules.map((module) =>
                    <CCLink
                      key={module.uuid}
                      url={urls.module}
                      params={{moduleId: module.uuid}}
                    >
                      <FlatButton
                        key={module.uuid}
                        style={style.moduleButton}
                        label={module.display_name ? module.display_name : module.uuid}
                        labelStyle={module.display_name ? {} : style.subtext}
                      />
                    </CCLink>
                  )}
                </TableRowColumn>
                <TableRowColumn>
                  <RaisedButton
                    label="Delete"
                    secondary={true}
                    disabled={schema.modules.size === 0 ? false : true}
                    onTouchTap={() => onDeleteTouchTap(schema)}
                  />
                </TableRowColumn>
              </TableRow>
            )
          })}
        </TableBody>
      </Table>
    )
  }
}

export default SchemasTable
