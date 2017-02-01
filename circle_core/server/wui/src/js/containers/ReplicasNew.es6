import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'

import ReplicationLinkNewPaper from '../components/ReplicationLinkNewPaper'


/**
 * ReplicationLonk作成
 */
class ReplicasNew extends Component {
  static propTypes = {
    location: PropTypes.object,
    modules: PropTypes.object.isRequired,
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
      modules,
      location,
    } = this.props
    const query = location.query

    return (
      <div className="page">
        <ReplicationLinkNewPaper
          modules={modules}
          selectedModuleId={query.module_id}
          onCreateTouchTap={() => console.log('ReplicationLinkNewPaper onCreateTouchTap')}
        />
      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  modules: state.entities.modules,
})

const mapDispatchToProps = (dispatch) => ({
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(ReplicasNew)
