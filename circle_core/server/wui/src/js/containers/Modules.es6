import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'

import FlatButton from 'material-ui/FlatButton'
import withWidth, {SMALL} from 'material-ui/utils/withWidth'

import actions from '../actions'
import {FloatingAddButton} from '../components/buttons'
import CCLink from '../components/CCLink'
import Fetching from '../components/Fetching'
import ModuleDeleteDialog from '../components/ModuleDeleteDialog'
import ModuleCards from '../components/Modules/ModuleCards'
import ModuleList from '../components/Modules/ModuleList'
import InputTextField from '../containers/InputTextField'
import {urls} from '../routes'


const TAB_CARDS = 'cards'
const TAB_LIST = 'list'

/**
 */
class Modules extends Component {
  static propTypes = {
    isFetching: PropTypes.bool.isRequired,
    isDeleteAsking: PropTypes.bool.isRequired,
    modules: PropTypes.object.isRequired,
    module: PropTypes.object.isRequired,
    inputText: PropTypes.string.isRequired,
    actions: PropTypes.object.isRequired,
    width: PropTypes.number.isRequired,
  }

  /**
   * @constructor
   */
  constructor(...args) {
    super(...args)

    this.state = {
      activeTab: TAB_CARDS,
    }
  }

  /**
   * @override
   */
  render() {
    const {
      isFetching,
      isDeleteAsking,
      modules,
      module,
      inputText,
      actions,
      width,
    } = this.props
    const {
      activeTab,
    } = this.state

    if(isFetching) {
      return (
        <Fetching />
      )
    }

    const filteredModules = inputText === '' ? modules : modules.filter((module) => (
      module.tags.filter((tag) => tag.includes(inputText)).size > 0
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

        <InputTextField
          hintText="タグでモジュールを絞込"
          fullWidth={true}
        />

        <div className="tabs">
          <div className="tab tabCards" style={{display: (activeTab === TAB_CARDS ? 'block' : 'none')}}>
            <ModuleCards
              modules={filteredModules}
              cols={width == SMALL ? 1 : 2}
            />
          </div>

          <div className="tab tabList" style={{display: (activeTab === TAB_LIST ? 'block' : 'none')}}>
            <ModuleList
              modules={filteredModules}
              onModulesTagTouchTap={actions.misc.inputTextChange}
              onModulesDeleteTouchTap={actions.modules.deleteAsk}
            />
          </div>
        </div>

        <CCLink url={urls.modulesNew}>
          <FloatingAddButton />
        </CCLink>

        <ModuleDeleteDialog
          isActive={isDeleteAsking}
          module={module}
          onOkTouchTap={actions.modules.deleteRequest}
          onCancelTouchTap={actions.modules.deleteCancel}
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
    isFetching: state.asyncs.isModulesFetching,
    isDeleteAsking: state.asyncs.isModulesDeleteAsking,
    modules: state.entities.modules,
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
      modules: bindActionCreators(actions.modules, dispatch),
      misc: bindActionCreators(actions.misc, dispatch),
    },
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(withWidth()(Modules))
