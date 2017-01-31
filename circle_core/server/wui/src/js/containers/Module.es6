import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'

import actions from 'src/actions'
import {urls} from 'src/routes'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'

import AddFloatingActionButton from 'src/components/commons/AddFloatingActionButton'
import CCLink from 'src/components/commons/CCLink'
import ModuleDeleteDialog from 'src/components/commons/ModuleDeleteDialog'

import ModuleDetail from 'src/components/ModuleDetail'


/**
 * Module詳細
 */
class Module extends Component {
  static propTypes = {
    isFetching: PropTypes.bool.isRequired,
    isUpdating: PropTypes.bool.isRequired,
    schemas: PropTypes.object.isRequired,
    modules: PropTypes.object.isRequired,
    params: PropTypes.object.isRequired,
    setTitle: PropTypes.func,
    onDeleteOkButtonTouchTap: PropTypes.func,
  }

  state = {
    isModuleDeleteDialogOpen: false,
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
   * @override
   */
  render() {
    const {
      isModuleDeleteDialogOpen,
    } = this.state
    const {
      isFetching,
      isUpdating,
      schemas,
      modules,
      params,
    } = this.props

    if (isFetching || isUpdating) {
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

    return (
      <div className="page">
        <ModuleDetail
          module={module}
          schemas={schemas}
          onMessageBoxDeleteTouchTap={(...args) => console.log('onMessageBoxDeleteTouchTap', ...args)}
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
      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  isFetching: state.asyncs.isModuleFetching,
  isUpdating: state.asyncs.isModulesUpdating,
  schemas: state.entities.schemas,
  modules: state.entities.modules,
})

const mapDispatchToProps = (dispatch) => ({
  setTitle: (title) => dispatch(actions.page.setTitle(title)),
  onDeleteOkButtonTouchTap: (module) => dispatch(actions.modules.deleteRequest(module.uuid)),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Module)
