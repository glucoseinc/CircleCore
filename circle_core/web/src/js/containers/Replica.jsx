import PropTypes from 'prop-types'
import React from 'react'
import {connect} from 'react-redux'

import actions from 'src/actions'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'

import ReplicationLinkDeleteDialog from 'src/components/commons/ReplicationLinkDeleteDialog'

import ReplicationLinkDetail from 'src/components/ReplicationLinkDetail'


/**
 * ReplicationLink詳細
 */
class Replica extends React.Component {
  static propTypes = {
    isFetching: PropTypes.bool.isRequired,
    replicationLinks: PropTypes.object.isRequired,
    modules: PropTypes.object.isRequired,
    ccInfos: PropTypes.object.isRequired,
    params: PropTypes.object.isRequired,
    setTitle: PropTypes.func,
    onDeleteOkButtonClick: PropTypes.func,
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
  onDeleteClick() {
    this.setState({
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
      isReplicationLinkDeleteDialogOpen,
    } = this.state
    const {
      isFetching,
      replicationLinks,
      modules,
      ccInfos,
      params,
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
          modules={modules}
          ccInfos={ccInfos}
          onDeleteClick={() => this.onDeleteClick()}
        />

        <ReplicationLinkDeleteDialog
          open={isReplicationLinkDeleteDialogOpen}
          replicationLink={replicationLink}
          onOkClick={(replicationLink) => this.onDeleteDialogButtonClick(true, replicationLink)}
          onCancelClick={() => this.onDeleteDialogButtonClick(false)}
        />
      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  isFetching: state.asyncs.isReplicationLinkFetching,
  replicationLinks: state.entities.replicationLinks,
  modules: state.entities.modules,
  ccInfos: state.entities.ccInfos,
})

const mapDispatchToProps = (dispatch) => ({
  setTitle: (title) => dispatch(actions.page.setTitle(title)),
  onDeleteOkButtonClick: (replicationLink) => dispatch(actions.replicationLink.deleteRequest(replicationLink.uuid)),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Replica)
