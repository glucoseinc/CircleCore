import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'

import FontIcon from 'material-ui/FontIcon'
import TextField from 'material-ui/TextField'

import actions from '../actions'

/**
 */
class InputTextField extends Component {
  static propTypes = {
    hintText: PropTypes.string,
    fullWidth: PropTypes.bool,
    inputText: PropTypes.string.isRequired,
    actions: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      hintText = null,
      fullWidth = false,
      inputText,
      actions,
    } = this.props

    const hintNode = (
      <span>
        <FontIcon className="material-icons" style={{color: 'inherit', verticalAlign: 'bottom'}}>search</FontIcon>
        {hintText}
      </span>
    )

    return (
      <div className="inputTextField">
        <TextField
          hintText={hintNode}
          fullWidth={fullWidth}
          value={inputText}
          onChange={(e) => actions.misc.inputTextChange(e.target.value)}
          hintStyle={{marginLeft: '32px'}}
          inputStyle={{marginLeft: '32px'}}
          underlineStyle={{bottom: '0'}}
        />
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
    inputText: state.misc.inputText,
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
      misc: bindActionCreators(actions.misc, dispatch),
    },
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(InputTextField)
