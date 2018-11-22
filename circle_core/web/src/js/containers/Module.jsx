import PropTypes from 'prop-types'
import React from 'react'
import {connect} from 'react-redux'
import {Set} from 'immutable'
import moment from 'moment'

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
class Module extends React.Component {
  static propTypes = {
    isModuleFetching: PropTypes.bool.isRequired,
    isModuleUpdating: PropTypes.bool.isRequired,
    schemas: PropTypes.object.isRequired,
    modules: PropTypes.object.isRequired,
    ccInfos: PropTypes.object.isRequired,
    token: PropTypes.object.isRequired,
    params: PropTypes.object.isRequired,
    setTitle: PropTypes.func,
    onUpdateClick: PropTypes.func,
    onDeleteOkButtonClick: PropTypes.func,
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
  onDeleteClick() {
    this.setState({
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
      isModuleDeleteDialogOpen: false,
    })
    if (execute && module) {
      this.props.onDeleteOkButtonClick(module)
    }
  }

  /**
   * MessageBox削除ボタン押下時の動作
   * @param {number} messageBoxIndex
   */
  onMessageBoxDeleteClick(messageBoxIndex) {
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
  onMessageBoxDeleteDialogButtonClick(execute, module) {
    this.setState({
      isMessageBoxDeleteDialogOpen: false,
      deleteMessageBoxIndex: null,
    })
    if (execute && module) {
      this.props.onUpdateClick(module)
    }
  }

  /**
   * MessageBoxダウンロードボタン押下時の動作
   * @param {object} module
   * @param {object} messageBox
   * @param {object} startDate
   * @param {object} endDate
   */
  async onMessageBoxDownloadClick(module, messageBox, startDate, endDate) {
    const params = {
      start: moment(startDate).format('YYYYMMDD'),
      end: moment(endDate).format('YYYYMMDD'),
      access_token: this.props.token.accessToken,
    }
    const query = Object.entries(params).map(([key, value]) => `${key}=${value}`).join('&')
    const url = `/download/${module.uuid}/${messageBox.uuid}/?${query}`
    window.open(url)
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
      ccInfos,
      params,
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
        <ModuleDetail
          module={module}
          schemas={schemas}
          ccInfos={ccInfos}
          tagSuggestions={tagSuggestions}
          attributeNameSuggestions={attributeNameSuggestions}
          attributeValueSuggestions={attributeValueSuggestions}
          onUpdateClick={this.props.onUpdateClick}
          onMessageBoxDeleteClick={(messageBoxIndex) => this.onMessageBoxDeleteClick(messageBoxIndex)}
          onMessageBoxDownloadClick={(...args) => this.onMessageBoxDownloadClick(...args)}
          onDeleteClick={::this.onDeleteClick}
        />

        <CCLink url={urls.replicasNew} params={params}>
          <AddFloatingActionButton />
        </CCLink>

        <ModuleDeleteDialog
          open={isModuleDeleteDialogOpen}
          module={module}
          onOkClick={(module) => this.onDeleteDialogButtonClick(true, module)}
          onCancelClick={() => this.onDeleteDialogButtonClick(false)}
        />

        {module && typeof deleteMessageBoxIndex === 'number' &&
          <MessageBoxDeleteDialog
            open={isMessageBoxDeleteDialogOpen}
            module={module}
            messageBoxIndex={deleteMessageBoxIndex}
            onOkClick={(messageBoxIndex) =>
              this.onMessageBoxDeleteDialogButtonClick(true, module.removeMessageBox(messageBoxIndex))}
            onCancelClick={() => this.onMessageBoxDeleteDialogButtonClick(false)}
          />
        }
      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  isModuleFetching: state.asyncs.isModuleFetching,
  isModuleUpdating: state.asyncs.isModuleUpdating,
  schemas: state.entities.schemas,
  modules: state.entities.modules,
  ccInfos: state.entities.ccInfos,
  token: state.auth.token,
})

const mapDispatchToProps = (dispatch) => ({
  setTitle: (title) => dispatch(actions.page.setTitle(title)),
  onUpdateClick: (module) => dispatch(actions.module.updateRequest(module.toJS())),
  onDeleteOkButtonClick: (module) => dispatch(actions.module.deleteRequest(module.uuid)),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Module)
