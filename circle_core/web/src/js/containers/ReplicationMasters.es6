import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'

import actions from 'src/actions'
import {urls} from 'src/routes'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'

import AddFloatingActionButton from 'src/components/commons/AddFloatingActionButton'
import CCLink from 'src/components/commons/CCLink'
import ReplicationMasterDeleteDialog from 'src/components/commons/ReplicationMasterDeleteDialog'

import ReplicactionMasterPaper from 'src/components/ReplicactionMasterPaper'


/**
 * 共有マスター一覧
 */
class ReplicactionMasters extends Component {
  static propTypes = {
    isReplicationMasterFetching: PropTypes.bool.isRequired,
    replicationMasters: PropTypes.object.isRequired,
    onDeleteOkButtonTouchTap: PropTypes.func,
  }

  state = {
    deleteReplicationMaster: null,
    isReplicationMasterDeleteDialogOpen: false,
  }

  /**
   * 追加メニュー 削除の選択時の動作
   * @param {object} replicationMaster
   */
  onDeleteTouchTap(replicationMaster) {
    this.setState({
      deleteReplicationMaster: replicationMaster,
      isReplicationMasterDeleteDialogOpen: true,
    })
  }

  /**
   * 削除ダイアログのボタン押下時の動作
   * @param {bool} execute
   * @param {object} replicationMaster
   */
  onDeleteDialogButtonTouchTap(execute, replicationMaster) {
    this.setState({
      deleteReplicationMaster: null,
      isReplicationMasterDeleteDialogOpen: false,
    })
    if (execute && replicationMaster) {
      this.props.onDeleteOkButtonTouchTap(replicationMaster)
    }
  }


  /**
   * @override
   */
  render() {
    const {
      deleteReplicationMaster,
      isReplicationMasterDeleteDialogOpen,
    } = this.state
    const {
      isReplicationMasterFetching,
      replicationMasters,
    } = this.props

    if (isReplicationMasterFetching) {
      return (
        <LoadingIndicator />
      )
    }

    return (
      <div className="page">
        {replicationMasters.valueSeq().map((repMaster) =>
          <ReplicactionMasterPaper
            key={repMaster.id}
            replicationMaster={repMaster}
            onDeleteTouchTap={::this.onDeleteTouchTap}
          />
        )}

        <CCLink url={urls.replicationMasterNew}>
          <AddFloatingActionButton />
        </CCLink>

        <ReplicationMasterDeleteDialog
          open={isReplicationMasterDeleteDialogOpen}
          replicationMaster={deleteReplicationMaster}
          onOkTouchTap={(replicationMaster) => this.onDeleteDialogButtonTouchTap(true, replicationMaster)}
          onCancelTouchTap={() => this.onDeleteDialogButtonTouchTap(false)}
        />

      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  isReplicationMasterFetching: state.asyncs.isReplicationMasterFetching,
  replicationMasters: state.entities.replicationMasters,
})

const mapDispatchToProps = (dispatch) => ({
  onDeleteOkButtonTouchTap: (replicationMaster) => {
    return dispatch(actions.replicationMaster.deleteRequest(replicationMaster.id))
  },
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(ReplicactionMasters)
