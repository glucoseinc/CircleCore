import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'

import actions from 'src/actions'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'

import ReplicationLinkNewPaper from 'src/components/ReplicationLinkNewPaper'


/**
 * ReplicationLonk作成
 */
class ReplicasNew extends Component {
  static propTypes = {
    isCreating: PropTypes.bool.isRequired,
    isModulesFetching: PropTypes.bool.isRequired,
    modules: PropTypes.object.isRequired,
    location: PropTypes.object,
    onCreateTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      isCreating,
      isModulesFetching,
      modules,
      location,
      onCreateTouchTap,
    } = this.props

    const moduleId = location.query.module_id
    if (moduleId === undefined) {
      return (
        <div>
          モジュールが選択されていません
        </div>
      )
    }

    if (isCreating || isModulesFetching) {
      return (
        <LoadingIndicator />
      )
    }

    const selectedModule = modules.get(moduleId)
    if (selectedModule === undefined) {
      return (
        <div>
          {moduleId}は存在しません
        </div>
      )
    }

    return (
      <div className="page">
        <ReplicationLinkNewPaper
          modules={modules}
          selectedModule={selectedModule}
          onCreateTouchTap={onCreateTouchTap}
        />
      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  isCreating: state.asyncs.isReplicationLinksCreating,
  isModulesFetching: state.asyncs.isModulesFetching,
  modules: state.entities.modules,
})

const mapDispatchToProps = (dispatch) => ({
  onCreateTouchTap: (replicationLink) => dispatch(actions.replicationLinks.createRequest(replicationLink.toJS())),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(ReplicasNew)
