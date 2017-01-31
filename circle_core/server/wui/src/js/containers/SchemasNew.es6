import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'

import actions from 'src/actions'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'

import SchemaNewPaper from 'src/components/SchemaNewPaper'


/**
 * Schema作成
 */
class SchemasNew extends Component {
  static propTypes = {
    isSchemaPropertyTypesFetching: PropTypes.bool.isRequired,
    schemaPropertyTypes: PropTypes.object.isRequired,
    onCreateTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      isSchemaPropertyTypesFetching,
      schemaPropertyTypes,
      onCreateTouchTap,
    } = this.props

    if (isSchemaPropertyTypesFetching) {
      return (
        <LoadingIndicator />
      )
    }

    return (
      <div className="page">
        <SchemaNewPaper
          propertyTypes={schemaPropertyTypes}
          onCreateTouchTap={onCreateTouchTap}
        />
      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  isSchemaPropertyTypesFetching: state.asyncs.isSchemaPropertyTypesFetching,
  schemaPropertyTypes: state.entities.schemaPropertyTypes,
})

const mapDispatchToProps = (dispatch) => ({
  onCreateTouchTap: (schema) => dispatch(actions.schemas.createRequest(schema.toJS())),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(SchemasNew)
