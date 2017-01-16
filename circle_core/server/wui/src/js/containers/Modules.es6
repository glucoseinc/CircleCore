import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'

import {GridList, GridTile} from 'material-ui/GridList'
import {Tabs, Tab} from 'material-ui/Tabs'
import TextField from 'material-ui/TextField'

import actions from '../actions'
import {AddButton} from '../components/buttons'
import CCLink from '../components/CCLink'
import Fetching from '../components/Fetching'
import ModuleDeleteDialog from '../components/ModuleDeleteDialog'
import ModulesTable from '../components/ModulesTable'
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

    const filteredModules = inputText === '' ? modules : modules.filter((module) => (
      module.tags.filter((tag) => tag.includes(inputText)).size > 0
    ))

    return (
      <Tabs
        contentContainerStyle={style.tab}
      >
        <Tab
          label="カード表示"
        >
        </Tab>
        <Tab
          label="リスト表示"
        >
          <GridList cols={12} cellHeight="auto">
            <GridTile cols={10}>
              <TextField
                hintText="タグで検索"
                fullWidth={true}
                value={inputText}
                onChange={(e) => actions.misc.inputTextChange(e.target.value)}
              />
            </GridTile>
            <GridTile cols={2}>
              <CCLink url={urls.modulesNew}>
                <AddButton />
              </CCLink>
            </GridTile>
          </GridList>

          <ModulesTable
            modules={filteredModules}
            onTagTouchTap={actions.misc.inputTextChange}
            onDeleteTouchTap={actions.modules.deleteAsk}
          />
          <ModuleDeleteDialog
            isActive={isDeleteAsking}
            module={module}
            onOkTouchTap={actions.modules.deleteRequest}
            onCancelTouchTap={actions.modules.deleteCancel}
          />
        </Tab>
      </Tabs>
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
