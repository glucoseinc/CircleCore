import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'

import actions from 'src/actions'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'

import ReplicationLinkNewPaper from 'src/components/ReplicationLinkNewPaper'


/**
 * ReplicationLink作成
 */
class ReplicasNew extends Component {
  static propTypes = {
    isReplicationLinkCreating: PropTypes.bool.isRequired,
    isModuleFetching: PropTypes.bool.isRequired,
    modules: PropTypes.object.isRequired,
    location: PropTypes.object,
    onCreateTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      isReplicationLinkCreating,
      isModuleFetching,
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

    if (isReplicationLinkCreating || isModuleFetching) {
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
  isReplicationLinkCreating: state.asyncs.isReplicationLinkCreating,
  isModuleFetching: state.asyncs.isModuleFetching,
  modules: state.entities.modules,
})

const mapDispatchToProps = (dispatch) => ({
  onCreateTouchTap: (replicationLink) => dispatch(actions.replicationLink.createRequest(replicationLink.toJS())),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(ReplicasNew)
