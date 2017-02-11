import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'
import {routerActions} from 'react-router-redux'

import withWidth from 'material-ui/utils/withWidth'

import actions from 'src/actions'
import {urls, createPathName} from 'src/routes'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'
import {ModuleIcon} from 'src/components/bases/icons'

import AddFloatingActionButton from 'src/components/commons/AddFloatingActionButton'
import CCLink from 'src/components/commons/CCLink'
import ModuleDeleteDialog from 'src/components/commons/ModuleDeleteDialog'

import Empty from 'src/components/Empty'
import ModulesTabComponent from 'src/components/ModulesTabComponent'


/**
 * Module一覧
 */
class Modules extends Component {
  static propTypes = {
    isModuleFetching: PropTypes.bool.isRequired,
    modules: PropTypes.object.isRequired,
    onModuleInfoPaperTouchTap: PropTypes.func,
    onIdCopyButtonTouchTap: PropTypes.func,
    onDeleteOkButtonTouchTap: PropTypes.func,
    width: PropTypes.number.isRequired,
  }

  state = {
    deleteModule: null,
    isModuleDeleteDialogOpen: false,
  }

  /**
   * 追加メニュー 削除の選択時の動作
   * @param {object} module
   */
  onDeleteTouchTap(module) {
    this.setState({
      deleteModule: module,
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
      deleteModule: null,
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
      deleteModule,
      isModuleDeleteDialogOpen,
    } = this.state
    const {
      isModuleFetching,
      modules,
      onModuleInfoPaperTouchTap,
      onIdCopyButtonTouchTap,
      width,
    } = this.props

    if (isModuleFetching) {
      return (
        <LoadingIndicator />
      )
    }

    return (
      <div>
        {modules.size === 0 ? (
          <Empty
            icon={ModuleIcon}
            itemName="モジュール"
          />
        ) : (
          <ModulesTabComponent
            modules={modules}
            width={width}
            onModuleInfoPaperTouchTap={onModuleInfoPaperTouchTap}
            onDeleteTouchTap={::this.onDeleteTouchTap}
            onIdCopyButtonTouchTap={onIdCopyButtonTouchTap}
          />
        )}

        <CCLink url={urls.modulesNew}>
          <AddFloatingActionButton />
        </CCLink>

        <ModuleDeleteDialog
          open={isModuleDeleteDialogOpen}
          module={deleteModule}
          onOkTouchTap={(module) => this.onDeleteDialogButtonTouchTap(true, module)}
          onCancelTouchTap={() => this.onDeleteDialogButtonTouchTap(false)}
        />
      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  isModuleFetching: state.asyncs.isModuleFetching,
  modules: state.entities.modules,
})

const mapDispatchToProps = (dispatch) => ({
  onModuleInfoPaperTouchTap: (moduleId) => dispatch(routerActions.push(createPathName(urls.module, {moduleId}))),
  onIdCopyButtonTouchTap: (uuid) => dispatch(actions.page.showSnackbar('IDをコピーしました')),
  onDeleteOkButtonTouchTap: (module) => dispatch(actions.module.deleteRequest(module.uuid)),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(withWidth()(Modules))
