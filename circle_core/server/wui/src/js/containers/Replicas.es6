import React, {Component, PropTypes} from 'react'
// import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'

// import actions from '../actions'

/**
 */
class Replicas extends Component {
  static propTypes = {
    actions: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  render() {
    return (
      <div>
        <h1>Not Implemented</h1>
      </div>
    )
  }
}


/**
 * [mapStateToProps description]
 * @param  {[type]} state [description]
 * @return {[type]}       [description]
 */
function mapStateToProps(state) {
  return {
  }
}

/**
 * [mapDispatchToProps description]
 * @param  {[type]} dispatch [description]
 * @return {[type]}          [description]
 */
function mapDispatchToProps(dispatch) {
  return {
    actions: {
    },
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Replicas)
