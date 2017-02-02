import React, {Component, PropTypes} from 'react'

import AutoComplete from 'material-ui/AutoComplete'

/**
 * タグテキストフィールド
 */
class TagTextField extends Component {
  static propTypes = {
    tag: PropTypes.string.isRequired,
    suggestions: PropTypes.array,
    onChange: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      tag,
      suggestions = [],
      onChange,
    } = this.props

    return (
      <AutoComplete
        floatingLabelText="タグ"
        dataSource={suggestions}
        searchText={tag}
        onUpdateInput={onChange}
      />
    )
  }
}

export default TagTextField
