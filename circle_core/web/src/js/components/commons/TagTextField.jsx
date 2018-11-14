import React, {Component, PropTypes} from 'react'

import AutoComplete from 'material-ui/AutoComplete'

/**
 * タグテキストフィールド
 */
class TagTextField extends Component {
  static propTypes = {
    tag: PropTypes.string.isRequired,
    suggestions: PropTypes.array,
    error: PropTypes.bool,
    onChange: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      tag,
      suggestions = [],
      error = false,
      onChange,
    } = this.props

    return (
      <AutoComplete
        floatingLabelText="タグ"
        dataSource={suggestions}
        searchText={tag}
        errorText={error ? 'タグが重複しています' : null}
        onUpdateInput={onChange}
      />
    )
  }
}

export default TagTextField
