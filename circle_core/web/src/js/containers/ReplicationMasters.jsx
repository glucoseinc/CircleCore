import PropTypes from 'prop-types'
import React from 'react'
import {connect} from 'react-redux'

import actions from 'src/actions'
import {urls} from 'src/routes'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'
import {CoreIcon} from 'src/components/bases/icons'

import AddFloatingActionButton from 'src/components/commons/AddFloatingActionButton'
import CCLink from 'src/components/commons/CCLink'
import ReplicationMasterDeleteDialog from 'src/components/commons/ReplicationMasterDeleteDialog'

import Empty from 'src/components/Empty'
import ReplicactionMasterPaper from 'src/components/ReplicactionMasterPaper'


/**
 * 共有マスター一覧
 */
class ReplicactionMasters extends React.Component {
  static propTypes = {
    isReplicationMasterFetching: PropTypes.bool.isRequired,
    replicationMasters: PropTypes.object.isRequired,
    onDeleteOkButtonClick: PropTypes.func,
  }

  state = {
    deleteReplicationMaster: null,
    isReplicationMasterDeleteDialogOpen: false,
  }

  /**
   * 追加メニュー 削除の選択時の動作
   * @param {object} replicationMaster
   */
  onDeleteClick(replicationMaster) {
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
  onDeleteDialogButtonClick(execute, replicationMaster) {
    this.setState({
      deleteReplicationMaster: null,
      isReplicationMasterDeleteDialogOpen: false,
    })
    if (execute && replicationMaster) {
      this.props.onDeleteOkButtonClick(replicationMaster)
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
      <div>
        {replicationMasters.size === 0 ? (
          <Empty
            icon={CoreIcon}
            itemName="共有マスター"
          />
        ) : (
          <div className="page">
            {replicationMasters.valueSeq().map((repMaster) => (
              <ReplicactionMasterPaper
                key={repMaster.id}
                replicationMaster={repMaster}
                onDeleteClick={::this.onDeleteClick}
              />
            ))}
          </div>
        )}

        <CCLink url={urls.replicationMasterNew}>
          <AddFloatingActionButton />
        </CCLink>

        <ReplicationMasterDeleteDialog
          open={isReplicationMasterDeleteDialogOpen}
          replicationMaster={deleteReplicationMaster}
          onOkClick={(replicationMaster) => this.onDeleteDialogButtonClick(true, replicationMaster)}
          onCancelClick={() => this.onDeleteDialogButtonClick(false)}
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
  onDeleteOkButtonClick: (replicationMaster) => {
    return dispatch(actions.replicationMaster.deleteRequest(replicationMaster.id))
  },
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(ReplicactionMasters)
