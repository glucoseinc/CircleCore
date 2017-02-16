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
    isSchemaFetching: PropTypes.bool.isRequired,
    isModuleFetching: PropTypes.bool.isRequired,
    schemas: PropTypes.object.isRequired,
    modules: PropTypes.object.isRequired,
    onCreateTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      isSchemaFetching,
      isModuleFetching,
      schemas,
      modules,
      onCreateTouchTap,
    } = this.props

    if (isSchemaFetching || isModuleFetching) {
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
  isSchemaFetching: state.asyncs.isSchemaFetching,
  isModuleFetching: state.asyncs.isModuleFetching,
  schemas: state.entities.schemas,
  modules: state.entities.modules,
})

const mapDispatchToProps = (dispatch) => ({
  onCreateTouchTap: (module) => dispatch(actions.module.createRequest(module.toJS())),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(ModulesNew)
