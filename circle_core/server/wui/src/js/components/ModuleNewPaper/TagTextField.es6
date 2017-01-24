import React, {Component, PropTypes} from 'react'

import TextField from 'material-ui/TextField'


/**
 */
class TagTextField extends Component {
  static propTypes = {
    tag: PropTypes.string.isRequired,
    onChange: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      tag,
      onChange,
    } = this.props

    return (
      <TextField
        floatingLabelText="タグ"
        value={tag}
        onChange={onChange}
      />
    )
  }
}

export default TagTextField
