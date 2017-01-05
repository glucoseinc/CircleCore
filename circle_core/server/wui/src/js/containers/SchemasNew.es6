import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'

import MenuItem from 'material-ui/MenuItem'
import RaisedButton from 'material-ui/RaisedButton'
import SelectField from 'material-ui/SelectField'
import {Table, TableBody, TableRow, TableRowColumn} from 'material-ui/Table'
import TextField from 'material-ui/TextField'

import * as actions from '../actions/schemasNew'
import {urls} from '../routes'
import CCLink from '../components/CCLink'
import Fetching from '../components/Fetching'

/**
 */
class SchemasNew extends Component {
  static propTypes = {
    schema: PropTypes.object,
    schemaPropertyTypes: PropTypes.array.isRequired,
    actions: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      isFetching,
      schema,
      schemaPropertyTypes,
      actions,
    } = this.props

    if (isFetching) {
      return (
        <Fetching />
      )
    }

    return (
      <div>
        <Table selectable={false}>
          <TableBody displayRowCheckbox={false}>
            <TableRow>
              <TableRowColumn>名前</TableRowColumn>
              <TableRowColumn>
                <TextField
                  name="displayName"
                  hintText="Option"
                  fullWidth={true}
                  value={schema.displayName}
                  onChange={(e) => actions.updateSchema(
                    schema.update('displayName', e.target.value)
                  )}
                />
              </TableRowColumn>
            </TableRow>
            <TableRow>
              <TableRowColumn>プロパティ</TableRowColumn>
              <TableRowColumn>
                <Table selectable={false}>
                  <TableBody displayRowCheckbox={false}>
                    {schema.properties.map((property, index) => {
                      return (
                        <TableRow key={index}>
                          <TableRowColumn>
                            <TextField
                              name="proparty-name"
                              floatingLabelText="name"
                              value={property.name}
                              onChange={(e) => actions.updateSchema(
                                schema.updateSchemaProperty(index, 'name', e.target.value)
                              )}
                            />
                          </TableRowColumn>
                          <TableRowColumn>
                            <SelectField
                              floatingLabelText="type"
                              value={property.type}
                              onChange={(e, i, v) => actions.updateSchema(
                                schema.updateSchemaProperty(index, 'type', v)
                              )}
                            >
                              {schemaPropertyTypes.map((schemaPropertyType) => {
                                return (
                                  <MenuItem
                                    key={schemaPropertyType.name}
                                    value={schemaPropertyType.name}
                                    primaryText={schemaPropertyType.name}
                                  />
                                )
                              })}
                            </SelectField>
                          </TableRowColumn>
                          <TableRowColumn>
                            <RaisedButton
                              label="Remove"
                              secondary={true}
                              disabled={schema.properties.size === 1 ? true : false}
                              onTouchTap={() => actions.updateSchema(
                                schema.removeSchemaProperty(index)
                              )}
                            />
                          </TableRowColumn>
                        </TableRow>
                      )
                    })}
                    <TableRow>
                      <TableRowColumn colSpan="3">
                        <RaisedButton
                          label="Add New Property"
                          primary={true}
                          onTouchTap={() => actions.updateSchema(
                            schema.pushSchemaProperty()
                          )}
                        />
                      </TableRowColumn>
                    </TableRow>
                  </TableBody>
                </Table>
              </TableRowColumn>
            </TableRow>
            <TableRow>
              <TableRowColumn>メタデータ</TableRowColumn>
              <TableRowColumn>
                <TextField
                  name="memo"
                  floatingLabelText="memo"
                  hintText="Option"
                  fullWidth={true}
                  multiLine={true}
                  rows={4}
                  rowsMax={4}
                  onChange={(e) => actions.updateSchema(
                    schema.updateSchemaMeta('memo', e.target.value)
                  )}
                />
              </TableRowColumn>
            </TableRow>
          </TableBody>
        </Table>
        <CCLink
          url={urls.schemas}
        >
          <RaisedButton
            label="Cancel"
            secondary={true}
          />
        </CCLink>
        <RaisedButton
          label="Create"
          primary={true}
          disabled={schema.isReadytoCreate() ? false : true}
          onTouchTap={() => actions.createTouchTap(schema)}
        />
      </div>
    )
  }
}

/**
 * [mapStateToProps description]
 * @param  {[type]} state [description]
 * @return {[type]}       [description]
 */
function mapStateToProps(state) {
  return {
    isFetching: state.asyncs.isSchemaPropertyFetching,
    schema: state.miscs.schema,
    schemaPropertyTypes: state.entities.schemaPropertyTypes,
  }
}

/**
 * [mapDispatchToProps description]
 * @param  {[type]} dispatch [description]
 * @return {[type]}          [description]
 */
function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(actions, dispatch),
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(SchemasNew)
