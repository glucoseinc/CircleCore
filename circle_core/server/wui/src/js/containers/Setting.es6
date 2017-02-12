import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'

import actions from 'src/actions'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'

import CcInfoEditPaper from 'src/components/CcInfoEditPaper'


/**
 * CircleCore情報変更
 */
class Setting extends Component {
  static propTypes = {
    isCcInfoFetching: PropTypes.bool.isRequired,
    isCcInfoUpdating: PropTypes.bool.isRequired,
    ccInfos: PropTypes.object.isRequired,
    onIdCopyButtonTouchTap: PropTypes.func,
    onUpdateTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      isCcInfoFetching,
      isCcInfoUpdating,
      ccInfos,
      onIdCopyButtonTouchTap,
      onUpdateTouchTap,
    } = this.props

    if (isCcInfoFetching || isCcInfoUpdating) {
      return (
        <LoadingIndicator />
      )
    }

    const ownCcInfo = ccInfos.filter((ccInfo) => ccInfo.myself).first()

    return (
      <div className="page">
        <CcInfoEditPaper
          ccInfo={ownCcInfo}
          onIdCopyButtonTouchTap={onIdCopyButtonTouchTap}
          onUpdateTouchTap={onUpdateTouchTap}
        />
      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  isCcInfoFetching: state.asyncs.isCcInfoFetching,
  isCcInfoUpdating: state.asyncs.isCcInfoUpdating,
  ccInfos: state.entities.ccInfos,
})

const mapDispatchToProps = (dispatch) => ({
  onUpdateTouchTap: (ccInfo) => dispatch(actions.ccInfo.updateRequest(ccInfo.toJS())),
  onIdCopyButtonTouchTap: (uuid) => dispatch(actions.page.showSnackbar('IDをコピーしました')),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Setting)
