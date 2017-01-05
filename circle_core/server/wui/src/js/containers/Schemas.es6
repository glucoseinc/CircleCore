import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'

import RaisedButton from 'material-ui/RaisedButton'

import * as actions from '../actions/schemas'
import {urls} from '../routes'
import Fetching from '../components/Fetching'
import CCLink from '../components/CCLink'
import SchemasTable from '../components/SchemasTable'
import SchemaDeleteDialog from '../components/SchemaDeleteDialog'

/**
 */
class Schemas extends Component {
  static propTypes = {
    isFetching: PropTypes.bool.isRequired,
    isDeleteAsking: PropTypes.bool.isRequired,
    schemas: PropTypes.array.isRequired,
    schema: PropTypes.object.isRequired,
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
      schema,
      actions,
    } = this.props

    if (isFetching) {
      return (
        <Fetching />
      )
    }

    return (
      <div>
        <CCLink url={urls.schemasNew}>
          <RaisedButton
            label="Add"
            primary={true}
          />
        </CCLink>

        <SchemasTable
          schemas={schemas}
          onDeleteTouchTap={actions.deleteTouchTap}
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
    schema: state.miscs.schema,
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
)(Schemas)
