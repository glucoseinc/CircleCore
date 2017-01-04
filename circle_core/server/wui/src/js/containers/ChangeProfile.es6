import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'

import RaisedButton from 'material-ui/RaisedButton'

import * as actions from '../actions/schemas'
import {urls} from '../routes'
import SchemasTable from '../components/SchemasTable'
import CCLink from '../components/CCLink'
import Fetching from '../components/Fetching'
import SchemaDeleteDialog from '../components/SchemaDeleteDialog'


/**
 */
class ChangeProfile extends Component {
  /**
   * @override
   */
  render() {

    return (
      <div>
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
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(ChangeProfile)
