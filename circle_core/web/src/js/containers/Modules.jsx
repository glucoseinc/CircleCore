import {routerActions} from 'connected-react-router'
import PropTypes from 'prop-types'
import React from 'react'
import {connect} from 'react-redux'

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
class Modules extends React.Component {
  static propTypes = {
    isModuleFetching: PropTypes.bool.isRequired,
    modules: PropTypes.object.isRequired,
    ccInfos: PropTypes.object.isRequired,
    onDisplayNameClick: PropTypes.func,
    onDeleteOkButtonClick: PropTypes.func,
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
  onDeleteClick(module) {
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
  onDeleteDialogButtonClick(execute, module) {
    this.setState({
      deleteModule: null,
      isModuleDeleteDialogOpen: false,
    })
    if (execute && module) {
      this.props.onDeleteOkButtonClick(module)
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
      ccInfos,
      onDisplayNameClick,
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
            ccInfos={ccInfos}
            width={width}
            onDisplayNameClick={(module) => onDisplayNameClick(module.uuid)}
            onDeleteClick={::this.onDeleteClick}
          />
        )}

        <CCLink url={urls.modulesNew}>
          <AddFloatingActionButton />
        </CCLink>

        <ModuleDeleteDialog
          open={isModuleDeleteDialogOpen}
          module={deleteModule}
          onOkClick={(module) => this.onDeleteDialogButtonClick(true, module)}
          onCancelClick={() => this.onDeleteDialogButtonClick(false)}
        />
      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  isModuleFetching: state.asyncs.isModuleFetching,
  modules: state.entities.modules,
  ccInfos: state.entities.ccInfos,
})

const mapDispatchToProps = (dispatch) => ({
  onDisplayNameClick: (moduleId) => dispatch(routerActions.push(createPathName(urls.module, {moduleId}))),
  onDeleteOkButtonClick: (module) => dispatch(actions.module.deleteRequest(module.uuid)),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(withWidth()(Modules))
