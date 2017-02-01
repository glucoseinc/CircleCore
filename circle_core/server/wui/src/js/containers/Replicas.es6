import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'

// import actions from 'src/actions'

import ReplicationLinkInfoPaper from 'src/components/ReplicationLinkInfoPaper'

/**
 */
class Replicas extends Component {
  static propTypes = {
    replicationLinks: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      replicationLinks,
    } = this.props

    return (
      <div className="page">
        {replicationLinks.valueSeq().map((replicationLink) =>
          <ReplicationLinkInfoPaper
            key={replicationLink.uuid}
            replicationLink={replicationLink}
          />
        )}
      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  replicationLinks: state.entities.replicationLinks,
})

const mapDispatchToProps = (dispatch) => ({
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Replicas)
