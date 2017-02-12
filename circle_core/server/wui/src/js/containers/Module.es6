import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'
import {Set} from 'immutable'

import actions from 'src/actions'
import {urls} from 'src/routes'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'

import AddFloatingActionButton from 'src/components/commons/AddFloatingActionButton'
import CCLink from 'src/components/commons/CCLink'
import MessageBoxDeleteDialog from 'src/components/commons/MessageBoxDeleteDialog'
import ModuleDeleteDialog from 'src/components/commons/ModuleDeleteDialog'

import ModuleDetail from 'src/components/ModuleDetail'


/**
 * Module詳細
 */
class Module extends Component {
  static propTypes = {
    isModuleFetching: PropTypes.bool.isRequired,
    isModuleUpdating: PropTypes.bool.isRequired,
    schemas: PropTypes.object.isRequired,
    modules: PropTypes.object.isRequired,
    params: PropTypes.object.isRequired,
    setTitle: PropTypes.func,
    onIdCopyButtonTouchTap: PropTypes.func,
    onUpdateTouchTap: PropTypes.func,
    onDeleteOkButtonTouchTap: PropTypes.func,
  }

  state = {
    isModuleDeleteDialogOpen: false,
    isMessageBoxDeleteDialogOpen: false,
    deleteMessageBoxIndex: null,
  }

  /**
   * @override
   */
  componentWillReceiveProps(nextProps) {
    const module = nextProps.modules.get(nextProps.params.moduleId)
    const title = module !== undefined ? module.label : ''
    this.props.setTitle(title)
  }

  /**
   * 削除ボタン押下時の動作
   */
  onDeleteTouchTap() {
    this.setState({
      isModuleDeleteDialogOpen: true,
    })
  }

  /**
   * 削除ダイアログのボタン押下時の動作
   * @param {bool} execute
   * @param {object} module
   */
  onDeleteDialogButtonTouchTap(execute, module) {
    this.setState({
      isModuleDeleteDialogOpen: false,
    })
    if (execute && module) {
      this.props.onDeleteOkButtonTouchTap(module)
    }
  }

  /**
   * MessageBox削除ボタン押下時の動作
   * @param {number} messageBoxIndex
   */
  onMessageBoxDeleteTouchTap(messageBoxIndex) {
    this.setState({
      isMessageBoxDeleteDialogOpen: true,
      deleteMessageBoxIndex: messageBoxIndex,
    })
  }

  /**
   * MessageBox削除ダイアログのボタン押下時の動作
   * @param {bool} execute
   * @param {object} module
   */
  onMessageBoxDeleteDialogButtonTouchTap(execute, module) {
    this.setState({
      isMessageBoxDeleteDialogOpen: false,
      deleteMessageBoxIndex: null,
    })
    if (execute && module) {
      this.props.onUpdateTouchTap(module)
    }
  }

  /**
   * @override
   */
  render() {
    const {
      isModuleDeleteDialogOpen,
      isMessageBoxDeleteDialogOpen,
      deleteMessageBoxIndex,
    } = this.state
    const {
      isModuleFetching,
      isModuleUpdating,
      schemas,
      modules,
      params,
      onIdCopyButtonTouchTap,
      onUpdateTouchTap,
    } = this.props

    if (isModuleFetching || isModuleUpdating) {
      return (
        <LoadingIndicator />
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

    const tagSuggestions = modules.reduce(
      (tagSet, module) => tagSet.union(module.tags)
      , new Set()
    ).toArray().sort()

    return (
      <div className="page">
        <ModuleDetail
          module={module}
          schemas={schemas}
          tagSuggestions={tagSuggestions}
          onIdCopyButtonTouchTap={onIdCopyButtonTouchTap}
          onUpdateTouchTap={onUpdateTouchTap}
          onMessageBoxDeleteTouchTap={(messageBoxIndex) => this.onMessageBoxDeleteTouchTap(messageBoxIndex)}
          onMessageBoxDownloadTouchTap={(...args) => console.log('onMessageBoxDownloadTouchTap', ...args)}
          onDeleteTouchTap={::this.onDeleteTouchTap}
        />

        <CCLink url={urls.replicasNew} params={params}>
          <AddFloatingActionButton />
        </CCLink>

        <ModuleDeleteDialog
          open={isModuleDeleteDialogOpen}
          module={module}
          onOkTouchTap={(module) => this.onDeleteDialogButtonTouchTap(true, module)}
          onCancelTouchTap={() => this.onDeleteDialogButtonTouchTap(false)}
        />

        <MessageBoxDeleteDialog
          open={isMessageBoxDeleteDialogOpen}
          module={module}
          messageBoxIndex={deleteMessageBoxIndex}
          onOkTouchTap={(messageBoxIndex) =>
            this.onMessageBoxDeleteDialogButtonTouchTap(true, module.removeMessageBox(messageBoxIndex))}
          onCancelTouchTap={() => this.onMessageBoxDeleteDialogButtonTouchTap(false)}
        />
      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  isModuleFetching: state.asyncs.isModuleFetching,
  isModuleUpdating: state.asyncs.isModuleUpdating,
  schemas: state.entities.schemas,
  modules: state.entities.modules,
})

const mapDispatchToProps = (dispatch) => ({
  setTitle: (title) => dispatch(actions.page.setTitle(title)),
  onIdCopyButtonTouchTap: (uuid) => dispatch(actions.page.showSnackbar('IDをコピーしました')),
  onUpdateTouchTap: (module) => dispatch(actions.module.updateRequest(module.toJS())),
  onDeleteOkButtonTouchTap: (module) => dispatch(actions.module.deleteRequest(module.uuid)),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Module)
