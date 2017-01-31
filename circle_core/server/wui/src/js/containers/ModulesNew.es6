import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'
import {Set} from 'immutable'

import actions from 'src/actions'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'

import ModuleNewPaper from 'src/components/ModuleNewPaper'


/**
 * Module作成
 */
class ModulesNew extends Component {
  static propTypes = {
    isSchemasFetching: PropTypes.bool.isRequired,
    isModulesFetching: PropTypes.bool.isRequired,
    schemas: PropTypes.object.isRequired,
    modules: PropTypes.object.isRequired,
    onCreateTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      isSchemasFetching,
      isModulesFetching,
      schemas,
      modules,
      onCreateTouchTap,
    } = this.props

    if (isSchemasFetching || isModulesFetching) {
      return (
        <LoadingIndicator />
      )
    }

    const tagSuggestions = modules.reduce(
      (tagSet, module) => tagSet.union(module.tags)
      , new Set()
    ).toArray().sort()

    return (
      <div className="page">
        <ModuleNewPaper
          schemas={schemas}
          tagSuggestions={tagSuggestions}
          onCreateTouchTap={onCreateTouchTap}
        />
      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  isSchemasFetching: state.asyncs.isSchemasFetching,
  isModulesFetching: state.asyncs.isModulesFetching,
  schemas: state.entities.schemas,
  modules: state.entities.modules,
})

const mapDispatchToProps = (dispatch) => ({
  onCreateTouchTap: (module) => dispatch(actions.modules.createRequest(module.toJS())),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(ModulesNew)
