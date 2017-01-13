import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'

import RaisedButton from 'material-ui/RaisedButton'

import actions from '../actions'
import {urls} from '../routes'
import CCLink from '../components/CCLink'
import Fetching from '../components/Fetching'

import {ModuleGeneralInfo, ModuleMetadataInfo, ModuleMessageBoxesInfo} from '../components/ModuleInfos'


/**
 */
class ModulesNew extends Component {
  static propTypes = {
    isSchemasFetching: PropTypes.bool.isRequired,
    schemas: PropTypes.object.isRequired,
    module: PropTypes.object.isRequired,
    inputText: PropTypes.string.isRequired,
    actions: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  componentWillMount() {
    const {
      actions,
    } = this.props
    actions.module.createInit()
    actions.schemas.fetchRequest()
  }


  /**
   * @override
   */
  render() {
    const {
      isSchemasFetching,
      schemas,
      module,
      inputText,
      actions,
    } = this.props

    if (isSchemasFetching) {
      return (
        <Fetching />
      )
    }

    return (
      <div>
        <ModuleGeneralInfo
          editable={true}
          module={module}
          actions={actions}
          hiddenUuid={true}
          hiddenActionsArea={true}
        />
        <ModuleMessageBoxesInfo
          editable={true}
          module={module}
          schemas={schemas}
          actions={actions}
          hiddenActionsArea={true}
        />
        <ModuleMetadataInfo
          editable={true}
          module={module}
          inputText={inputText}
          actions={actions}
          hiddenActionsArea={true}
        />
        <CCLink
          url={urls.modules}
        >
          <RaisedButton
            label="Cancel"
            secondary={true}
          />
        </CCLink>
        <RaisedButton
          label="Create"
          primary={true}
          disabled={module.isReadytoCreate() ? false : true}
          onTouchTap={() => actions.modules.createRequest(module)}
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
    isSchemasFetching: state.asyncs.isSchemasFetching,
    schemas: state.entities.schemas,
    module: state.misc.module,
    inputText: state.misc.inputText,
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
      modules: bindActionCreators(actions.modules, dispatch),
      module: bindActionCreators(actions.module, dispatch),
      misc: bindActionCreators(actions.misc, dispatch),
    },
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(ModulesNew)
