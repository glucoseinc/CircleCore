import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'

import CcInfoPaper from 'src/components/CcInfoPaper'

/**
 * CircleCore一覧
 */
class Cores extends Component {
  static propTypes = {
    isCcInfoFetching: PropTypes.bool.isRequired,
    ccInfos: PropTypes.object.isRequired,
  }

  state = {
  }

  /**
   * @override
   */
  render() {
    // const {
    // } = this.state
    const {
      isCcInfoFetching,
      ccInfos,
    } = this.props

    if (isCcInfoFetching) {
      return (
        <LoadingIndicator />
      )
    }

    // remove myself
    const foreignCcInfos = ccInfos.filter((ccInfo) => !ccInfo.myself)

    return (
      <div className="page">
        {foreignCcInfos.valueSeq().map((ccInfo) =>
          <CcInfoPaper
            key={ccInfo.uuid}
            ccInfo={ccInfo}
            onDisplayNameTouchTap={
              () => console.log('onDisplayNameTouchTap')}
            onDeleteTouchTap={
              () => console.log('onDeleteTouchTap')}
          />
        )}
      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  isCcInfoFetching: state.asyncs.isCcInfoFetching,
  ccInfos: state.entities.ccInfos,
})

const mapDispatchToProps = (dispatch) => ({
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Cores)
