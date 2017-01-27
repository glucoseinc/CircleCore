import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'

import actions from '../actions'
import Fetching from '../components/Fetching'
import ModuleNewPaper from '../components/ModuleNewPaper'


/**
 * Module作成
 */
class ModulesNew extends Component {
  static propTypes = {
    isSchemasFetching: PropTypes.bool.isRequired,
    schemas: PropTypes.object.isRequired,
    onCreateTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      isSchemasFetching,
      schemas,
      onCreateTouchTap,
    } = this.props

    if (isSchemasFetching) {
      return (
        <Fetching />
      )
    }

    return (
      <div className="page">
        <ModuleNewPaper
          schemas={schemas}
          onCreateTouchTap={onCreateTouchTap}
        />
      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  isSchemasFetching: state.asyncs.isSchemasFetching,
  schemas: state.entities.schemas,
})

const mapDispatchToProps = (dispatch) => ({
  onCreateTouchTap: (module) => dispatch(actions.modules.createRequest(module.toJS())),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(ModulesNew)
