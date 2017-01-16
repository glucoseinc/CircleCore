import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'

import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn} from 'material-ui/Table'

import actions from '../actions'
import {urls} from '../routes'
import CCLink from '../components/CCLink'
import Fetching from '../components/Fetching'
import SchemaDeleteDialog from '../components/SchemaDeleteDialog'
import {BackButton, RemoveButton} from '../components/buttons'


/**
 */
class Schema extends Component {
  static propTypes = {
    isFetching: PropTypes.bool.isRequired,
    isDeleteAsking: PropTypes.bool.isRequired,
    schemas: PropTypes.object.isRequired,
    params: PropTypes.object.isRequired,
    actions: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  componentWillMount() {
    const {
      params,
      actions,
    } = this.props
    actions.schema.fetchRequest(params.schemaId)
  }

  /**
   * @override
   */
  render() {
    const {
      isFetching,
      isDeleteAsking,
      schemas,
      params,
      actions,
    } = this.props

    if (isFetching) {
      return (
        <Fetching />
      )
    }

    const schema = schemas.get(params.schemaId)

    if (schema === undefined) {
      return (
        <div>
          {params.schemaId}は存在しません
        </div>
      )
    }

    return (
      <div>
        <Table selectable={false}>
          <TableBody displayRowCheckbox={false}>
            <TableRow>
              <TableRowColumn>名前</TableRowColumn>
              <TableRowColumn>{schema.displayName}</TableRowColumn>
            </TableRow>
            <TableRow>
              <TableRowColumn>UUID</TableRowColumn>
              <TableRowColumn>{schema.uuid}</TableRowColumn>
            </TableRow>
            <TableRow>
              <TableRowColumn>プロパティ</TableRowColumn>
              <TableRowColumn>
                <Table selectable={false}>
                  <TableHeader displaySelectAll={false} adjustForCheckbox={false}>
                    <TableRow>
                      <TableHeaderColumn>Name</TableHeaderColumn>
                      <TableHeaderColumn>Type</TableHeaderColumn>
                    </TableRow>
                  </TableHeader>

                  <TableBody displayRowCheckbox={false}>
                    {schema.properties.map((property, index) =>
                      <TableRow key={index}>
                        <TableRowColumn>{property.name}</TableRowColumn>
                        <TableRowColumn>{property.type}</TableRowColumn>
                      </TableRow>
                    )}
                  </TableBody>
                </Table>
              </TableRowColumn>
            </TableRow>
            <TableRow>
              <TableRowColumn>メタデータ</TableRowColumn>
              <TableRowColumn>
                <p>メモ</p>
                <p>{schema.memo}</p>
              </TableRowColumn>
            </TableRow>
          </TableBody>
        </Table>
        <CCLink
          url={urls.schemas}
        >
          <BackButton />
        </CCLink>
        <RemoveButton
          disabled={schema.modules.size === 0 ? false : true}
          onTouchTap={() => actions.schemas.deleteAsk(schema)}
        />
        <SchemaDeleteDialog
          isActive={isDeleteAsking}
          schema={schema}
          onOkTouchTap={actions.schemas.deleteRequest}
          onCancelTouchTap={actions.schemas.deleteCancel}
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
    isFetching: state.asyncs.isSchemaFetching,
    isDeleteAsking: state.asyncs.isSchemasDeleteAsking,
    schemas: state.entities.schemas,
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
    },
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Schema)
