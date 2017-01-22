import React, {Component, PropTypes} from 'react'

import TextField from 'material-ui/TextField'


/**
 */
class MemoTextField extends Component {
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

    const verticalShift = -24

    const style = {
      root: {
        height: 144 + verticalShift,
      },
      floatingLabel: {
        top: 38 + verticalShift,
      },
      textarea: {
        marginTop: 36 + verticalShift,
        marginBottom: -36 + verticalShift,
      },
    }

    return (
      <TextField
        floatingLabelText="メモ"
        fullWidth={true}
        multiLine={true}
        rows={4}
        rowsMax={4}
        value={schema.memo}
        onChange={onChange}
        style={style.root}
        floatingLabelStyle={style.floatingLabel}
        textareaStyle={style.textarea}
      />
    )
  }
}

export default MemoTextField
