import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'

import {GridList, GridTile} from 'material-ui/GridList'
import RaisedButton from 'material-ui/RaisedButton'
import TextField from 'material-ui/TextField'

import actions from '../actions/modules'
import {urls} from '../routes'
import Fetching from '../components/Fetching'
import CCLink from '../components/CCLink'
import ModulesTable from '../components/ModulesTable'
import ModuleDeleteDialog from '../components/ModuleDeleteDialog'

/**
 */
class Modules extends Component {
  static propTypes = {
    isFetching: PropTypes.bool.isRequired,
    isDeleteAsking: PropTypes.bool.isRequired,
    modules: PropTypes.array.isRequired,
    module: PropTypes.object.isRequired,
    searchText: PropTypes.string.isRequired,
    actions: PropTypes.object.isRequired,
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
      searchText,
      actions,
    } = this.props

    if (isFetching) {
      return (
        <Fetching />
      )
    }

    const filteredModules = searchText === '' ? modules : modules.filter((module) => (
      module.metadata.tags.filter((tag) => tag.includes(searchText)).size > 0
    ))

    return (
      <div>
        <GridList cols={12} cellHeight="auto">
          <GridTile cols={10}>
            <TextField
              hintText="Search by tag"
              fullWidth={true}
              value={searchText}
              onChange={(e) => actions.searchTextChange(e.target.value)}
            />
          </GridTile>
          <GridTile cols={2}>
            <CCLink url={urls.modulesNew}>
              <RaisedButton
                label="Add"
                primary={true}
              />
            </CCLink>
          </GridTile>
        </GridList>

        <ModulesTable
          modules={filteredModules}
          onTagTouchTap={actions.tagTouchTap}
          onDeleteTouchTap={actions.deleteTouchTap}
        />
        <ModuleDeleteDialog
          isActive={isDeleteAsking}
          module={module}
          onOkTouchTap={actions.deleteExecuteTouchTap}
          onCancelTouchTap={actions.deleteCancelTouchTap}
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
    isDeleteAsking: state.asyncs.isModuleDeleteAsking,
    modules: state.entities.modules,
    module: state.miscs.module,
    searchText: state.miscs.searchText,
  }
}

/**
 * [mapDispatchToProps description]
 * @param  {[type]} dispatch [description]
 * @return {[type]}          [description]
 */
function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(actions, dispatch),
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Modules)
