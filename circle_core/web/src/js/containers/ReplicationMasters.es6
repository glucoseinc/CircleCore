import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'

import actions from 'src/actions'
import {urls} from 'src/routes'
import LoadingIndicator from 'src/components/bases/LoadingIndicator'
import CCLink from 'src/components/commons/CCLink'
import AddFloatingActionButton from 'src/components/commons/AddFloatingActionButton'
import ReplicactionMasterPaper from 'src/components/ReplicactionMasterPaper'

/**
 * 共有マスター
 */
class ReplicactionMasters extends Component {
  static propTypes = {
    isReplicationMasterFetching: PropTypes.bool.isRequired,
    replicationMasters: PropTypes.object.isRequired,
    onDeleteReplicationMaster: PropTypes.func.isRequired,
  }

  /**
   * @override
   */
  render() {
    if(this.props.isReplicationMasterFetching) {
      return (
        <LoadingIndicator />
      )
    }

    // const {
    // } = this.state
    const {
      replicationMasters,
    } = this.props

    return (
      <div className="page">
        {replicationMasters.valueSeq().map((repMaster) =>
          <ReplicactionMasterPaper
            key={repMaster.id}
            replicationMaster={repMaster}
            onDeleteTouchTap={this.props.onDeleteReplicationMaster}
          />
        )}

        <CCLink url={urls.replicationMasterNew}>
          <AddFloatingActionButton />
        </CCLink>

      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  isReplicationMasterFetching: state.asyncs.isReplicationMasterFetching,
  replicationMasters: state.entities.replicationMasters,
})

const mapDispatchToProps = (dispatch) => ({
  onDeleteReplicationMaster: (replicationMaster) => {
    return dispatch(actions.replicationMaster.deleteRequest(replicationMaster.id))
  },
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(ReplicactionMasters)
