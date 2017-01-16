import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'

import actions from '../actions'
import {AddButton, RemoveButton} from '../components/buttons'
import Fetching from '../components/Fetching'
import ModuleDeleteDialog from '../components/ModuleDeleteDialog'
import {ModuleGeneralInfo, ModuleMetadataInfo, ModuleMessageBoxesInfo} from '../components/ModuleInfos'

/**
 */
class Module extends Component {
  static propTypes = {
    isFetching: PropTypes.bool.isRequired,
    isUpdating: PropTypes.bool.isRequired,
    isDeleteAsking: PropTypes.bool.isRequired,
    schemas: PropTypes.object.isRequired,
    modules: PropTypes.object.isRequired,
    tempModule: PropTypes.object.isRequired,
    moduleEditingArea: PropTypes.string.isRequired,
    inputText: PropTypes.string.isRequired,
    params: PropTypes.object.isRequired,
    actions: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  componentWillMount() {
    const {
      params,
      actions,
    } = this.props
    actions.module.fetchRequest(params.moduleId)
    actions.schemas.fetchRequest()
  }

  /**
   * @override
   */
  render() {
    const {
      isFetching,
      isUpdating,
      isDeleteAsking,
      schemas,
      modules,
      tempModule,
      moduleEditingArea,
      inputText,
      params,
      actions,
    } = this.props

    const style = {
      contentHeader: {
        display: 'flex',
        justifyContent: 'flex-end',
      },
      contentFooter: {
        display: 'flex',
        justifyContent: 'center',
      },
    }
    if (isFetching || isUpdating) {
      return (
        <Fetching />
      )
    }

    const module = modules.get(params.moduleId)

    if (module === undefined) {
      return (
        <div>
          {params.moduleId}は存在しません
        </div>
      )
    }

    const isEditingGeneral = moduleEditingArea === 'general'
    const isEditingMetadata = moduleEditingArea === 'metadata'
    const isEditingMessageBox = moduleEditingArea === 'messageBox'

    return (
      <div>
        <div style={style.contentHeader}>
          <AddButton
            label="共有リンクを作成する"
            onOkTouchTap={() => actions.shareLinks.createRequest()}
          />
        </div>

        <ModuleGeneralInfo
          editable={isEditingGeneral}
          module={isEditingGeneral ? tempModule : module}
          actions={actions}
          hiddenUuid={false}
          hiddenActionsArea={false}
        />
        <ModuleMetadataInfo
          editable={isEditingMetadata}
          module={isEditingMetadata ? tempModule : module}
          inputText={inputText}
          actions={actions}
          hiddenActionsArea={false}
        />
        <ModuleMessageBoxesInfo
          editable={isEditingMessageBox}
          module={isEditingMessageBox ? tempModule : module}
          schemas={schemas}
          actions={actions}
          hiddenActionsArea={false}
        />

        <ModuleDeleteDialog
          isActive={isDeleteAsking}
          module={module}
          onOkTouchTap={actions.modules.deleteRequest}
          onCancelTouchTap={actions.modules.deleteCancel}
        />

        <div style={style.contentFooter}>
          <RemoveButton
            label="このモジュールを削除する"
            onTouchTap={() => actions.modules.deleteAsk(module)}
          />
        </div>
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
    isFetching: state.asyncs.isModuleFetching,
    isUpdating: state.asyncs.isModulesUpdating,
    isDeleteAsking: state.asyncs.isModulesDeleteAsking,
    schemas: state.entities.schemas,
    modules: state.entities.modules,
    tempModule: state.misc.module,
    moduleEditingArea: state.misc.moduleEditingArea,
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
      shareLinks: bindActionCreators(actions.shareLinks, dispatch),
      misc: bindActionCreators(actions.misc, dispatch),
    },
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Module)
