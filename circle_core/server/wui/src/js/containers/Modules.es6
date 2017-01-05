import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'

import RaisedButton from 'material-ui/RaisedButton'

import * as actions from '../actions/modules'
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
      actions,
    } = this.props

    if (isFetching) {
      return (
        <Fetching />
      )
    }

    return (
      <div>
        <CCLink url={urls.modulesNew}>
          <RaisedButton
            label="Add"
            primary={true}
          />
        </CCLink>

        <ModulesTable
          modules={modules}
          onMessageBoxTouchTap={actions.messageBoxTouchTap}
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
