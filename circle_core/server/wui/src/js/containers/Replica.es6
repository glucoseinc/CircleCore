import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'

import actions from 'src/actions'


/**
 * ReplicationLink詳細
 */
class Replica extends Component {
  static propTypes = {
  }

  /**
   * @override
   */
  render() {
    const {
    } = this.props

    return (
      <div className="page">
      </div>
    )
  }
}


const mapStateToProps = (state) => ({
})

const mapDispatchToProps = (dispatch) => ({
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Replica)
