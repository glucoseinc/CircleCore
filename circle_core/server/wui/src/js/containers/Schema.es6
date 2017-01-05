import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'

import RaisedButton from 'material-ui/RaisedButton'
import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn} from 'material-ui/Table'

import * as actions from '../actions/schema'
import {urls} from '../routes'
import CCLink from '../components/CCLink'
import Fetching from '../components/Fetching'
import SchemaDeleteDialog from '../components/SchemaDeleteDialog'

/**
 */
class Schema extends Component {
  static propTypes = {
    isFetching: PropTypes.bool.isRequired,
    isDeleteAsking: PropTypes.bool.isRequired,
    schemas: PropTypes.array.isRequired,
    params: PropTypes.object.isRequired,
    actions: PropTypes.object.isRequired,
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

    const schema = schemas.filter((_schema) => _schema.uuid === params.schemaId)[0]

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
                    {schema.properties.map((property, index) => {
                      return (
                        <TableRow key={index}>
                          <TableRowColumn>{property.name}</TableRowColumn>
                          <TableRowColumn>{property.type}</TableRowColumn>
                        </TableRow>
                      )
                    })}
                  </TableBody>
                </Table>
              </TableRowColumn>
            </TableRow>
            <TableRow>
              <TableRowColumn>メタデータ</TableRowColumn>
              <TableRowColumn>
                <p>メモ</p>
                <p>{schema.metadata.memo}</p>
              </TableRowColumn>
            </TableRow>
          </TableBody>
        </Table>
        <CCLink
          url={urls.schemas}
        >
          <RaisedButton
            label="Back"
          />
        </CCLink>
        <RaisedButton
          label="Delete"
          secondary={true}
          disabled={schema.modules.size === 0 ? false : true}
          onTouchTap={actions.deleteTouchTap}
        />
        <SchemaDeleteDialog
          isActive={isDeleteAsking}
          schema={schema}
          onOkTouchTap={actions.deleteExecuteTouchTap}
          onCancelTouchTap={actions.deleteCancelTouchTap}
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
    isFetching: state.asyncs.isSchemasFetching,
    isDeleteAsking: state.asyncs.isSchemaDeleteAsking,
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
    actions: bindActionCreators(actions, dispatch),
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Schema)