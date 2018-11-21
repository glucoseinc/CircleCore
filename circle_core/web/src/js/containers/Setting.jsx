import PropTypes from 'prop-types'
import React from 'react'
import {connect} from 'react-redux'

import actions from 'src/actions'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'

import CcInfoEditPaper from 'src/components/CcInfoEditPaper'


/**
 * CircleCore情報変更
 */
class Setting extends React.Component {
  static propTypes = {
    isCcInfoFetching: PropTypes.bool.isRequired,
    isCcInfoUpdating: PropTypes.bool.isRequired,
    ccInfos: PropTypes.object.isRequired,
    onUpdateClick: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      isCcInfoFetching,
      isCcInfoUpdating,
      ccInfos,
      onUpdateClick,
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
          onUpdateClick={onUpdateClick}
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
  onUpdateClick: (ccInfo) => dispatch(actions.ccInfo.updateRequest(ccInfo.toJS())),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Setting)
