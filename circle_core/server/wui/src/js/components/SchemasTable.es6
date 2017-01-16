import React, {Component, PropTypes} from 'react'

import FlatButton from 'material-ui/FlatButton'
import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn} from 'material-ui/Table'
import {blueGrey600} from 'material-ui/styles/colors'

import {RemoveButton} from '../components/buttons'
import CCLink from '../components/CCLink'
import {urls} from '../routes'


/**
 */
class SchemasTable extends Component {
  static propTypes = {
    schemas: PropTypes.object.isRequired,
    modules: PropTypes.object.isRequired,
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
      modules,
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
      <Table>
        <TableHeader
          displaySelectAll={false}
          adjustForCheckbox={false}
        >
          <TableRow>
            <TableHeaderColumn tooltip="Schema name">名前</TableHeaderColumn>
            <TableHeaderColumn tooltip="Modules using schema">モジュール</TableHeaderColumn>
            <TableHeaderColumn></TableHeaderColumn>
          </TableRow>
        </TableHeader>

        <TableBody
          displayRowCheckbox={false}
        >
          {schemas.sort(sortComparator).valueSeq().map((schema) =>
            <TableRow key={schema.uuid}>
              <TableRowColumn>
                <CCLink
                  url={urls.schema}
                  params={{schemaId: schema.uuid}}
                >
                  {schema.displayName}<br/>
                  <span style={style.subtext}>{schema.uuid}</span>
                </CCLink>
              </TableRowColumn>
              <TableRowColumn>
                {schema.modules.map((moduleId) => {
                  const module = modules.get(moduleId)
                  return (
                    <CCLink
                      key={module.uuid}
                      url={urls.module}
                      params={{moduleId: moduleId}}
                    >
                      <FlatButton
                        key={module.uuid}
                        style={style.moduleButton}
                        label={module.label}
                        labelStyle={module.displayName ? {} : style.subtext}
                      />
                    </CCLink>
                  )
                })}
              </TableRowColumn>
              <TableRowColumn>
                <RemoveButton
                  disabled={schema.modules.size === 0 ? false : true}
                  onTouchTap={() => onDeleteTouchTap(schema)}
                />
              </TableRowColumn>
            </TableRow>
          )}
        </TableBody>
      </Table>
    )
  }
}

export default SchemasTable
