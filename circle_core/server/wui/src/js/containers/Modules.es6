import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'
import {routerActions} from 'react-router-redux'

import FlatButton from 'material-ui/FlatButton'
import withWidth, {SMALL} from 'material-ui/utils/withWidth'

import actions from '../actions'
import {FloatingAddButton} from '../components/buttons'
import CCLink from '../components/CCLink'
import Fetching from '../components/Fetching'
import ModuleDeleteDialog from '../components/ModuleDeleteDialog'
import ModuleCards from '../components/Modules/ModuleCards'
import ModuleInfoPaper from '../components/ModuleInfoPaper'
import SearchTextField from '../components/commons/SearchTextField'
import {urls, createPathName} from '../routes'

const TAB_CARDS = 'cards'
const TAB_LIST = 'list'


/**
 * Module一覧
 */
class Modules extends Component {
  static propTypes = {
    isFetching: PropTypes.bool.isRequired,
    modules: PropTypes.object.isRequired,
    onModuleInfoPaperTouchTap: PropTypes.func,
    onDeleteOkButtonTouchTap: PropTypes.func,
    width: PropTypes.number.isRequired,
  }

  state = {
    activeTab: TAB_CARDS,
    searchText: '',
    deleteModule: null,
    isModuleDeleteDialogOpen: false,
  }

  /**
   * 検索テキストを更新
   * @param {string} newText
   */
  setSearchText(newText) {
    this.setState({
      searchText: newText,
    })
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
    console.log('onDeleteDialogButtonTouchTap', execute, module)
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
      activeTab,
      searchText,
      deleteModule,
      isModuleDeleteDialogOpen,
    } = this.state
    const {
      isFetching,
      modules,
      onModuleInfoPaperTouchTap,
      width,
    } = this.props

    if(isFetching) {
      return (
        <Fetching />
      )
    }

    const filteredModules = searchText === '' ? modules : modules.filter((module) => (
      module.tags.filter((tag) => tag.includes(searchText)).size > 0
    ))

    return (
      <div className="page pageModules">

        <div className="pageModules-tabs">
          <div className={`pageModules-tab ${activeTab === TAB_CARDS ? 'is-active' : ''}`}>
            <FlatButton
              label="カード表示"
              onTouchTap={() => this.setState({activeTab: TAB_CARDS})}
            />
          </div>
          <div className={`pageModules-tab ${activeTab === TAB_LIST ? 'is-active' : ''}`}>
            <FlatButton
              label="リスト表示"
              onTouchTap={() => this.setState({activeTab: TAB_LIST})}
            />
          </div>
        </div>

        <SearchTextField
          hintText="タグでモジュールを絞込"
          fullWidth={true}
          inputText={searchText}
          onChange={::this.setSearchText}
        />

        <div className="tabs">
          <div className="tab tabCards" style={{display: (activeTab === TAB_CARDS ? 'block' : 'none')}}>
            <ModuleCards
              modules={filteredModules}
              cols={width == SMALL ? 1 : 2}
            />
          </div>

          <div className="tab tabList" style={{display: (activeTab === TAB_LIST ? 'block' : 'none')}}>
            {filteredModules.valueSeq().map((module) =>
              <ModuleInfoPaper
                key={module.uuid}
                module={module}
                onTouchTap={(module) => onModuleInfoPaperTouchTap(module.uuid)}
                onTagButtonTouchTap={(tag) => this.setSearchText(tag)}
                onDeleteTouchTap={::this.onDeleteTouchTap}
              />
            )}
          </div>
        </div>

        <CCLink url={urls.modulesNew}>
          <FloatingAddButton />
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
  isFetching: state.asyncs.isModulesFetching,
  modules: state.entities.modules,
})

const mapDispatchToProps = (dispatch) => ({
  onModuleInfoPaperTouchTap: (moduleId) => dispatch(routerActions.push(createPathName(urls.module, {moduleId}))),
  onDeleteOkButtonTouchTap: (module) => dispatch(actions.modules.deleteRequest(module)),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(withWidth()(Modules))
