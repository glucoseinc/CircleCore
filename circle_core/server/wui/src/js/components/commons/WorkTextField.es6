import React, {Component, PropTypes} from 'react'

import TextField from 'material-ui/TextField'


/**
 * 所属テキストフィールド
 */
class WorkTextField extends Component {
  static propTypes = {
    obj: PropTypes.object.isRequired,
    floatingLabelText: PropTypes.string,
    onChange: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      obj,
      floatingLabelText = '所属',
      onChange,
    } = this.props

    return (
      <TextField
        floatingLabelText={floatingLabelText}
        fullWidth={true}
        value={obj.work}
        onChange={onChange}
      />
    )
  }
}

export default WorkTextField
