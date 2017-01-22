import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'

import MenuItem from 'material-ui/MenuItem'
import SelectField from 'material-ui/SelectField'
import {Table, TableBody, TableRow, TableRowColumn} from 'material-ui/Table'
import TextField from 'material-ui/TextField'

import actions from '../actions'
import {AddButton, CancelButton, CreateButton, RemoveButton} from '../components/buttons'
import CCLink from '../components/CCLink'
import Fetching from '../components/Fetching'
import {urls} from '../routes'


/**
 */
class SchemasNew extends Component {
  static propTypes = {
    isSchemaPropertyTypesFetching: PropTypes.bool.isRequired,
    schema: PropTypes.object.isRequired,
    schemaPropertyTypes: PropTypes.object.isRequired,
    actions: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      isSchemaPropertyTypesFetching,
      schema,
      schemaPropertyTypes,
      actions,
    } = this.props

    if (isSchemaPropertyTypesFetching) {
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
                  hintText="オプション"
                  fullWidth={true}
                  value={schema.displayName}
                  onChange={(e) => actions.schema.update(
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
                    {schema.properties.map((property, index) =>
                      <TableRow key={index}>
                        <TableRowColumn>
                          <TextField
                            name="proparty-name"
                            floatingLabelText="属性名"
                            value={property.name}
                            onChange={(e) => actions.schema.update(
                              schema.updateSchemaProperty(index, 'name', e.target.value)
                            )}
                          />
                        </TableRowColumn>
                        <TableRowColumn>
                          <SelectField
                            floatingLabelText="属性タイプ"
                            value={property.type}
                            onChange={(e, i, v) => actions.schema.update(
                              schema.updateSchemaProperty(index, 'type', v)
                            )}
                          >
                            {schemaPropertyTypes.valueSeq().map((schemaPropertyType) =>
                              <MenuItem
                                key={schemaPropertyType.name}
                                value={schemaPropertyType.name}
                                primaryText={schemaPropertyType.name}
                              />
                            )}
                          </SelectField>
                        </TableRowColumn>
                        <TableRowColumn>
                          <RemoveButton
                            disabled={schema.properties.size === 1 ? true : false}
                            onTouchTap={() => actions.schema.update(
                              schema.removeSchemaProperty(index)
                            )}
                          />
                        </TableRowColumn>
                      </TableRow>
                    )}
                    <TableRow>
                      <TableRowColumn colSpan="3">
                        <AddButton
                          onTouchTap={() => actions.schema.update(
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
                  floatingLabelText="メモ"
                  hintText="Option"
                  fullWidth={true}
                  multiLine={true}
                  rows={4}
                  rowsMax={4}
                  value={schema.memo}
                  onChange={(e) => actions.schema.update(
                    schema.update('memo', e.target.value)
                  )}
                />
              </TableRowColumn>
            </TableRow>
          </TableBody>
        </Table>
        <CCLink url={urls.schemas}>
          <CancelButton />
        </CCLink>
        <CreateButton
          disabled={schema.isReadytoCreate() ? false : true}
          onTouchTap={() => actions.schemas.createRequest(schema)}
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
    isSchemaPropertyTypesFetching: state.asyncs.isSchemaPropertyTypesFetching,
    schema: state.misc.schema,
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
    actions: {
      schemas: bindActionCreators(actions.schemas, dispatch),
      schema: bindActionCreators(actions.schema, dispatch),
      schemaPropertyTypes: bindActionCreators(actions.schemaPropertyTypes, dispatch),
    },
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(SchemasNew)
