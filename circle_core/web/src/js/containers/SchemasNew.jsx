import PropTypes from 'prop-types'
import React from 'react'
import {connect} from 'react-redux'

import actions from 'src/actions'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'

import SchemaNewPaper from 'src/components/SchemaNewPaper'


/**
 * Schema作成
 */
class SchemasNew extends React.Component {
  static propTypes = {
    isSchemaFetching: PropTypes.bool.isRequired,
    isSchemaPropertyTypeFetching: PropTypes.bool.isRequired,
    schemaPropertyTypes: PropTypes.object.isRequired,
    schemas: PropTypes.object.isRequired,
    location: PropTypes.object.isRequired,
    onCreateTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      isSchemaFetching,
      isSchemaPropertyTypeFetching,
      schemas,
      schemaPropertyTypes,
      location,
      onCreateTouchTap,
    } = this.props

    const schemaId = location.query.schema_id
    let schema
    if (schemaId !== undefined) {
      if (isSchemaFetching) {
        return (
          <LoadingIndicator />
        )
      }
      schema = schemas.get(schemaId)
    }

    if (isSchemaPropertyTypeFetching) {
      return (
        <LoadingIndicator />
      )
    }

    return (
      <div className="page">
        <SchemaNewPaper
          templateSchema={schema}
          propertyTypes={schemaPropertyTypes}
          onCreateTouchTap={onCreateTouchTap}
        />
      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  isSchemaFetching: state.asyncs.isSchemaFetching,
  isSchemaPropertyTypeFetching: state.asyncs.isSchemaPropertyTypeFetching,
  schemas: state.entities.schemas,
  schemaPropertyTypes: state.entities.schemaPropertyTypes,
})

const mapDispatchToProps = (dispatch) => ({
  onCreateTouchTap: (schema) => dispatch(actions.schema.createRequest(schema.toJS())),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(SchemasNew)
