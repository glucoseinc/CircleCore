import React, {Component, PropTypes} from 'react'

import TextField from 'material-ui/TextField'


/**
 */
class DisplayNameTextField extends Component {
  static propTypes = {
    schema: PropTypes.object.isRequired,
    onChange: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      schema,
      onChange,
    } = this.props

    return (
      <TextField
        floatingLabelText="メッセージスキーマ名"
        fullWidth={true}
        value={schema.displayName}
        onChange={onChange}
      />
    )
  }
}

export default DisplayNameTextField
