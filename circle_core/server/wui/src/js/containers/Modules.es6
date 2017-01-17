import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'

import {Tabs, Tab} from 'material-ui/Tabs'

import actions from '../actions'
import Fetching from '../components/Fetching'
import ModuleDeleteDialog from '../components/ModuleDeleteDialog'
import ModulesCard from '../components/Modules/ModulesCard'
import ModulesList from '../components/Modules/ModulesList'


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
  }

  /**
   * @override
   */
  componentWillMount() {
    const {
      actions,
    } = this.props
    actions.modules.fetchRequest()
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

    return (
      <div>
        <Tabs
          contentContainerStyle={style.tab}
        >
          <Tab
            label="カード表示"
          >
            <ModulesCard
              modules={modules}
            />
          </Tab>
          <Tab
            label="リスト表示"
          >
            <ModulesList
              modules={modules}
              inputText={inputText}
              onModulesTagTouchTap={actions.misc.inputTextChange}
              onModulesDeleteTouchTap={actions.modules.deleteAsk}
            />
          </Tab>
        </Tabs>

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
)(Modules)
