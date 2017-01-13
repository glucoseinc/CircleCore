import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'

import RaisedButton from 'material-ui/RaisedButton'

import actions from '../actions'
import {urls} from '../routes'
import CCLink from '../components/CCLink'
import Fetching from '../components/Fetching'
import SchemaDeleteDialog from '../components/SchemaDeleteDialog'
import SchemasTable from '../components/SchemasTable'


/**
 */
class Schemas extends Component {
  static propTypes = {
    isFetching: PropTypes.bool.isRequired,
    isDeleteAsking: PropTypes.bool.isRequired,
    schemas: PropTypes.object.isRequired,
    modules: PropTypes.object.isRequired,
    schema: PropTypes.object.isRequired,
    actions: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  componentWillMount() {
    const {
      actions,
    } = this.props
    actions.schemas.fetchRequest()
  }

  /**
   * @override
   */
  render() {
    const {
      isFetching,
      isDeleteAsking,
      schemas,
      modules,
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
          modules={modules}
          onDeleteTouchTap={actions.schemas.deleteAsk}
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
    isFetching: state.asyncs.isSchemasFetching,
    isDeleteAsking: state.asyncs.isSchemasDeleteAsking,
    schemas: state.entities.schemas,
    modules: state.entities.modules,
    schema: state.misc.schema,
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
    },
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Schemas)
