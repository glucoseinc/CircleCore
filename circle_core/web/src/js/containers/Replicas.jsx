import {routerActions} from 'connected-react-router'
import PropTypes from 'prop-types'
import React from 'react'
import {connect} from 'react-redux'

import actions from 'src/actions'
import {urls, createPathName} from 'src/routes'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'
import {ReplicationLinkIcon} from 'src/components/bases/icons'

import ReplicationLinkDeleteDialog from 'src/components/commons/ReplicationLinkDeleteDialog'

import Empty from 'src/components/Empty'
import ReplicationLinkInfoPaper from 'src/components/ReplicationLinkInfoPaper'


/**
 * ReplicationLink一覧
 */
class Replicas extends React.Component {
  static propTypes = {
    isReplicationLinkFetching: PropTypes.bool.isRequired,
    replicationLinks: PropTypes.object.isRequired,
    modules: PropTypes.object.isRequired,
    ccInfos: PropTypes.object.isRequired,
    onDisplayNameClick: PropTypes.func,
    onDeleteOkButtonClick: PropTypes.func,
  }

  state = {
    deleteReplicationLink: null,
    isReplicationLinkDeleteDialogOpen: false,
  }

  /**
   * 追加メニュー 削除の選択時の動作
   * @param {object} replicationLink
   */
  onDeleteClick(replicationLink) {
    this.setState({
      deleteReplicationLink: replicationLink,
      isReplicationLinkDeleteDialogOpen: true,
    })
  }

  /**
   * 削除ダイアログのボタン押下時の動作
   * @param {bool} execute
   * @param {object} replicationLink
   */
  onDeleteDialogButtonClick(execute, replicationLink) {
    this.setState({
      deleteReplicationLink: null,
      isReplicationLinkDeleteDialogOpen: false,
    })
    if (execute && replicationLink) {
      this.props.onDeleteOkButtonClick(replicationLink)
    }
  }

  /**
   * @override
   */
  render() {
    const {
      deleteReplicationLink,
      isReplicationLinkDeleteDialogOpen,
    } = this.state
    const {
      isReplicationLinkFetching,
      replicationLinks,
      modules,
      ccInfos,
      onDisplayNameClick,
    } = this.props

    if (isReplicationLinkFetching) {
      return (
        <LoadingIndicator />
      )
    }

    return (
      <div>
        {replicationLinks.size === 0 ? (
          <Empty
            icon={ReplicationLinkIcon}
            itemName="共有リンク"
          />
        ) : (
          <div className="page">
            <div className="replicationLinks">
              {replicationLinks.valueSeq().map((replicationLink) => (
                <ReplicationLinkInfoPaper
                  key={replicationLink.uuid}
                  replicationLink={replicationLink}
                  modules={modules}
                  ccInfos={ccInfos}
                  onDeleteClick={::this.onDeleteClick}
                  onDisplayNameClick={onDisplayNameClick}
                />
              ))}
            </div>
          </div>
        )}

        <ReplicationLinkDeleteDialog
          open={isReplicationLinkDeleteDialogOpen}
          replicationLink={deleteReplicationLink}
          onOkClick={(replicationLink) => this.onDeleteDialogButtonClick(true, replicationLink)}
          onCancelClick={() => this.onDeleteDialogButtonClick(false)}
        />
      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  isReplicationLinkFetching: state.asyncs.isReplicationLinkFetching,
  replicationLinks: state.entities.replicationLinks,
  modules: state.entities.modules,
  ccInfos: state.entities.ccInfos,
})

const mapDispatchToProps = (dispatch) => ({
  onDisplayNameClick: (replicationLinkId) => (
    dispatch(routerActions.push(createPathName(urls.replica, {replicationLinkId})))
  ),
  onDeleteOkButtonClick: (replicationLink) => dispatch(actions.replicationLink.deleteRequest(replicationLink.uuid)),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Replicas)
