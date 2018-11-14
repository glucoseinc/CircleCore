import React, {Component, PropTypes} from 'react'

import TextField from 'material-ui/TextField'


/**
 * 表示名テキストフィールド
 */
class DisplayNameTextField extends Component {
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
      floatingLabelText = '表示名',
      onChange,
      ...other
    } = this.props

    return (
      <TextField
        floatingLabelText={floatingLabelText}
        fullWidth={true}
        value={obj.displayName}
        onChange={onChange}
        {...other}
      />
    )
  }
}

export default DisplayNameTextField
