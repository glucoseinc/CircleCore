import PropTypes from 'prop-types'
import React from 'react'
import TextField from 'material-ui/TextField'


/**
 * メモテキストフィールド
 */
class MemoTextField extends React.Component {
  static propTypes = {
    obj: PropTypes.object.isRequired,
    onChange: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      obj,
      onChange,
    } = this.props

    const verticalShift = -8

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
        value={obj.memo}
        onChange={onChange}
        style={style.root}
        floatingLabelStyle={style.floatingLabel}
        textareaStyle={style.textarea}
      />
    )
  }
}

export default MemoTextField
