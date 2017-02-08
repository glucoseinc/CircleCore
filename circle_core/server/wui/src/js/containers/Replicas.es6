import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'
import {routerActions} from 'react-router-redux'

import actions from 'src/actions'
import {urls, createPathName} from 'src/routes'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'

import ReplicationLinkDeleteDialog from 'src/components/commons/ReplicationLinkDeleteDialog'

import ReplicationLinkInfoPaper from 'src/components/ReplicationLinkInfoPaper'


/**
 * ReplicationLink一覧
 */
class Replicas extends Component {
  static propTypes = {
    isFetching: PropTypes.bool.isRequired,
    replicationLinks: PropTypes.object.isRequired,
    modules: PropTypes.object.isRequired,
    ccInfos: PropTypes.object.isRequired,
    onDisplayNameTouchTap: PropTypes.func,
    onUrlCopyButtonTouchTap: PropTypes.func,
    onReplicationSlaveCopyButtonTouchTap: PropTypes.func,
    onDeleteOkButtonTouchTap: PropTypes.func,
  }

  state = {
    deleteReplicationLink: null,
    isReplicationLinkDeleteDialogOpen: false,
  }

  /**
   * 追加メニュー 削除の選択時の動作
   * @param {object} replicationLink
   */
  onDeleteTouchTap(replicationLink) {
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
  onDeleteDialogButtonTouchTap(execute, replicationLink) {
    this.setState({
      deleteReplicationLink: null,
      isReplicationLinkDeleteDialogOpen: false,
    })
    if (execute && replicationLink) {
      this.props.onDeleteOkButtonTouchTap(replicationLink)
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
      isFetching,
      replicationLinks,
      modules,
      ccInfos,
      onDisplayNameTouchTap,
      onUrlCopyButtonTouchTap,
      onReplicationSlaveCopyButtonTouchTap,
    } = this.props

    if (isFetching) {
      return (
        <LoadingIndicator />
      )
    }

    return (
      <div className="page">
        {replicationLinks.valueSeq().map((replicationLink) =>
          <ReplicationLinkInfoPaper
            key={replicationLink.uuid}
            replicationLink={replicationLink}
            modules={modules}
            ccInfos={ccInfos}
            onDisplayNameTouchTap={(replicationLink) => onDisplayNameTouchTap(replicationLink.uuid)}
            onUrlCopyButtonTouchTap={onUrlCopyButtonTouchTap}
            onReplicationSlaveCopyButtonTouchTap={onReplicationSlaveCopyButtonTouchTap}
            onDeleteTouchTap={::this.onDeleteTouchTap}
          />
        )}

        <ReplicationLinkDeleteDialog
          open={isReplicationLinkDeleteDialogOpen}
          replicationLink={deleteReplicationLink}
          onOkTouchTap={(replicationLink) => this.onDeleteDialogButtonTouchTap(true, replicationLink)}
          onCancelTouchTap={() => this.onDeleteDialogButtonTouchTap(false)}
        />
      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  isFetching: state.asyncs.isReplicationLinksFetching,
  replicationLinks: state.entities.replicationLinks,
  modules: state.entities.modules,
  ccInfos: state.entities.ccInfos,
})

const mapDispatchToProps = (dispatch) => ({
  onDisplayNameTouchTap: (replicationLinkId) => (
    dispatch(routerActions.push(createPathName(urls.replica, {replicationLinkId})))
  ),
  onUrlCopyButtonTouchTap: (url) => dispatch(actions.page.showSnackbar('URLをコピーしました')),
  onReplicationSlaveCopyButtonTouchTap: (uuid) => dispatch(actions.page.showSnackbar('IDをコピーしました')),
  onDeleteOkButtonTouchTap: (replicationLink) => dispatch(actions.replicationLinks.deleteRequest(replicationLink.uuid)),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Replicas)
