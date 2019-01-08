import PropTypes from 'prop-types'
import React from 'react'
import {connect} from 'react-redux'

import actions from 'src/actions'
import LoadingIndicator from 'src/components/bases/LoadingIndicator'
import ReplicationLinkNewPaper from 'src/components/ReplicationLinkNewPaper'
import {searchStringToQuery} from 'src/routes'


/**
 * ReplicationLink作成
 */
class ReplicasNew extends React.Component {
  static propTypes = {
    isReplicationLinkCreating: PropTypes.bool.isRequired,
    isModuleFetching: PropTypes.bool.isRequired,
    modules: PropTypes.object.isRequired,
    location: PropTypes.object,
    onCreateClick: PropTypes.func,
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
      onCreateClick,
    } = this.props

    const query = searchStringToQuery(location.search)
    const moduleId = query.module_id
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
          onCreateClick={onCreateClick}
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
  onCreateClick: (replicationLink) => dispatch(actions.replicationLink.createRequest(replicationLink.toJS())),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(ReplicasNew)
