import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'

import actions from 'src/actions'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'

import ReplicationLinkDeleteDialog from 'src/components/commons/ReplicationLinkDeleteDialog'

import ReplicationLinkDetail from 'src/components/ReplicationLinkDetail'


/**
 * ReplicationLink詳細
 */
class Replica extends Component {
  static propTypes = {
    isFetching: PropTypes.bool.isRequired,
    replicationLinks: PropTypes.object.isRequired,
    messageBoxes: PropTypes.object.isRequired,
    modules: PropTypes.object.isRequired,
    ccInfos: PropTypes.object.isRequired,
    params: PropTypes.object.isRequired,
    setTitle: PropTypes.func,
    onUrlCopyButtonTouchTap: PropTypes.func,
    onReplicationSlaveCopyButtonTouchTap: PropTypes.func,
    onDeleteOkButtonTouchTap: PropTypes.func,
  }

  state = {
    isReplicationLinkDeleteDialogOpen: false,
  }

  /**
   * @override
   */
  componentWillReceiveProps(nextProps) {
    const replicationLink = nextProps.replicationLinks.get(nextProps.params.replicationLinkId)
    const title = replicationLink !== undefined ? replicationLink.label : ''
    this.props.setTitle(title)
  }

  /**
   * 削除ボタン押下時の動作
   */
  onDeleteTouchTap() {
    this.setState({
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
      isReplicationLinkDeleteDialogOpen,
    } = this.state
    const {
      isFetching,
      replicationLinks,
      messageBoxes,
      modules,
      ccInfos,
      params,
      onUrlCopyButtonTouchTap,
      onReplicationSlaveCopyButtonTouchTap,
    } = this.props

    if (isFetching) {
      return (
        <LoadingIndicator />
      )
    }

    const replicationLink = replicationLinks.get(params.replicationLinkId)

    if (replicationLink === undefined) {
      return (
        <div>
          {params.replicationLinkId}は存在しません
        </div>
      )
    }

    return (
      <div className="page">
        <ReplicationLinkDetail
          replicationLink={replicationLink}
          messageBoxes={messageBoxes}
          modules={modules}
          ccInfos={ccInfos}
          onUrlCopyButtonTouchTap={onUrlCopyButtonTouchTap}
          onReplicationSlaveCopyButtonTouchTap={onReplicationSlaveCopyButtonTouchTap}
          onDeleteTouchTap={() => this.onDeleteTouchTap()}
        />

        <ReplicationLinkDeleteDialog
          open={isReplicationLinkDeleteDialogOpen}
          replicationLink={replicationLink}
          onOkTouchTap={(replicationLink) => this.onDeleteDialogButtonTouchTap(true, replicationLink)}
          onCancelTouchTap={() => this.onDeleteDialogButtonTouchTap(false)}
        />
      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  isFetching: state.asyncs.isReplicationLinkFetching,
  replicationLinks: state.entities.replicationLinks,
  messageBoxes: state.entities.messageBoxes,
  modules: state.entities.modules,
  ccInfos: state.entities.ccInfos,
})

const mapDispatchToProps = (dispatch) => ({
  setTitle: (title) => dispatch(actions.page.setTitle(title)),
  onUrlCopyButtonTouchTap: (url) => dispatch(actions.page.showSnackbar('URLをコピーしました')),
  onReplicationSlaveCopyButtonTouchTap: (uuid) => dispatch(actions.page.showSnackbar('IDをコピーしました')),
  onDeleteOkButtonTouchTap: (replicationLink) => dispatch(actions.replicationLinks.deleteRequest(replicationLink.uuid)),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Replica)
