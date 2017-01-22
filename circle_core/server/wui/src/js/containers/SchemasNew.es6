import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'

import actions from '../actions'
import Fetching from '../components/Fetching'
import SchemaNewPaper from '../components/SchemaNewPaper'


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
        <Fetching />
      )
    }

    return (
      <div>
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
  onCreateTouchTap: (schema) => dispatch(actions.schemas.createRequest(schema)),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(SchemasNew)
