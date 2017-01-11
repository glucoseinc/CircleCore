import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'

import {GridList, GridTile} from 'material-ui/GridList'
import RaisedButton from 'material-ui/RaisedButton'
import TextField from 'material-ui/TextField'

import actions from '../actions'
import {urls} from '../routes'
import CCLink from '../components/CCLink'
import Fetching from '../components/Fetching'
import ModuleDeleteDialog from '../components/ModuleDeleteDialog'
import ModulesTable from '../components/ModulesTable'


/**
 */
class Modules extends Component {
  static propTypes = {
    isFetching: PropTypes.bool.isRequired,
    isDeleteAsking: PropTypes.bool.isRequired,
    modules: PropTypes.array.isRequired,
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

    if (isFetching) {
      return (
        <Fetching />
      )
    }

    const filteredModules = inputText === '' ? modules : modules.filter((module) => (
      module.tags.filter((tag) => tag.includes(inputText)).size > 0
    ))

    return (
      <div>
        <GridList cols={12} cellHeight="auto">
          <GridTile cols={10}>
            <TextField
              hintText="Search by tag"
              fullWidth={true}
              value={inputText}
              onChange={(e) => actions.misc.inputTextChange(e.target.value)}
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
          onTagTouchTap={actions.misc.inputTextChange}
          onDeleteTouchTap={actions.modules.deleteAsk}
        />
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
