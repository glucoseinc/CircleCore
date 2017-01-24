import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'

import {Tabs, Tab} from 'material-ui/Tabs'
import withWidth, {SMALL} from 'material-ui/utils/withWidth'

import actions from '../actions'
import {FloatingAddButton} from '../components/buttons'
import CCLink from '../components/CCLink'
import Fetching from '../components/Fetching'
import ModuleDeleteDialog from '../components/ModuleDeleteDialog'
import ModulesCards from '../components/Modules/ModulesCards'
import ModulesList from '../components/Modules/ModulesList'
import InputTextField from '../containers/InputTextField'
import {urls} from '../routes'


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

    const style = {
      tab: {
        paddingTop: 16,
        paddingLeft: 24,
        paddingRight: 24,
        paddingbottom: 16,
      },
    }

    if (isFetching) {
      return (
        <Fetching />
      )
    }

    const filteredModules = inputText === '' ? modules : modules.filter((module) => (
      module.tags.filter((tag) => tag.includes(inputText)).size > 0
    ))

    return (
      <div className="page pageModules">
        <Tabs
          contentContainerStyle={style.tab}
        >
          <Tab
            label="カード表示"
          >
            <InputTextField
              hintText="タグで検索"
              fullWidth={true}
            />

            <ModulesCards
              modules={filteredModules}
              cols={width == SMALL ? 1 : 2}
            />
          </Tab>
          <Tab
            label="リスト表示"
          >
            <InputTextField
              hintText="タグで検索"
              fullWidth={true}
            />
            <ModulesList
              modules={filteredModules}
              onModulesTagTouchTap={actions.misc.inputTextChange}
              onModulesDeleteTouchTap={actions.modules.deleteAsk}
            />
          </Tab>
        </Tabs>

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
