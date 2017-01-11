import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'

import * as actions from '../actions/modulesNew'

/**
 */
class ModulesNew extends Component {
  static propTypes = {
    actions: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  render() {
    return (
      <div>
        <h1>ModulesNew</h1>
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
)(ModulesNew)
