import React, {Component, PropTypes} from 'react'

import TextField from 'material-ui/TextField'

import {SearchIcon} from 'src/components/bases/icons'


/**
 * 検索テキストフィールド
 */
class SearchTextField extends Component {
  static propTypes = {
    hintText: PropTypes.string,
    fullWidth: PropTypes.bool,
    inputText: PropTypes.string.isRequired,
    onChange: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      hintText = null,
      fullWidth = false,
      inputText,
      onChange,
    } = this.props

    const hintNode = (
      <span>
        <SearchIcon style={{color: 'inherit', verticalAlign: 'bottom'}} />
        {hintText}
      </span>
    )

    return (
      <div className="searchTextField">
        <TextField
          hintText={hintNode}
          fullWidth={fullWidth}
          value={inputText}
          onChange={(e) => onChange(e.target.value)}
          hintStyle={{marginLeft: '32px'}}
          inputStyle={{marginLeft: '32px'}}
          underlineStyle={{bottom: '0'}}
        />
      </div>
    )
  }
}


export default SearchTextField
