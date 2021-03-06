import PropTypes from 'prop-types'
import React from 'react'
import {connect} from 'react-redux'
import {Set} from 'immutable'

import actions from 'src/actions'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'

import ModuleNewPaper from 'src/components/ModuleNewPaper'


/**
 * Module作成
 */
class ModulesNew extends React.Component {
  static propTypes = {
    isSchemaFetching: PropTypes.bool.isRequired,
    isModuleFetching: PropTypes.bool.isRequired,
    schemas: PropTypes.object.isRequired,
    modules: PropTypes.object.isRequired,
    onCreateClick: PropTypes.func,
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
      onCreateClick,
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

    const attributeNameSuggestions = modules.reduce(
      (attributeNameSet, module) => attributeNameSet.union(module.attributes.map((attribute) => attribute.name))
      , new Set()
    ).toArray().sort()

    const attributeValueSuggestions = modules.reduce(
      (attributeNameSet, module) => attributeNameSet.union(module.attributes.map((attribute) => attribute.value))
      , new Set()
    ).toArray().sort()

    return (
      <div className="page">
        <ModuleNewPaper
          schemas={schemas}
          tagSuggestions={tagSuggestions}
          attributeNameSuggestions={attributeNameSuggestions}
          attributeValueSuggestions={attributeValueSuggestions}
          onCreateClick={onCreateClick}
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
  onCreateClick: (module) => dispatch(actions.module.createRequest(module.toJS())),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(ModulesNew)
