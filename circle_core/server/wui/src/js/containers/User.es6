import React, {PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'

import actions from '../actions'
// import {urls} from '../routes'
// import CCLink from '../components/CCLink'
import Fetching from '../components/Fetching'


/**
 */
class User extends React.Component {
  static propTypes = {
    isFetching: PropTypes.bool.isRequired,
    // isDeleteAsking: PropTypes.bool.isRequired,
    users: PropTypes.array.isRequired,
    actions: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  componentWillMount() {
    const {
      actions,
    } = this.props
    actions.users.fetchRequest()
  }

  /**
   * @override
   */
  render() {
    const {
      isFetching,
      users,
      params,
      // actions,
    } = this.props

    if (isFetching) {
      return (
        <Fetching />
      )
    }

    const user = users.find((x) => x.uuid === params.userId)

    return (
      <div>
        {user.mailAddress}
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
    isFetching: state.asyncs.isUsersFetching,
    users: state.entities.users,
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
      users: bindActionCreators(actions.users, dispatch),
    },
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(User)
