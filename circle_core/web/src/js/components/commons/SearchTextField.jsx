import PropTypes from 'prop-types'
import React from 'react'

import AutoComplete from 'material-ui/AutoComplete'
import IconButton from 'material-ui/IconButton'
import Paper from 'material-ui/Paper'

import {ClearIcon, SearchIcon} from 'src/components/bases/icons'


/**
 * 検索テキストフィールド
 */
class SearchTextField extends React.Component {
  static propTypes = {
    hintText: PropTypes.string,
    fullWidth: PropTypes.bool,
    inputText: PropTypes.string.isRequired,
    suggestions: PropTypes.array,
    onChange: PropTypes.func,
  }
  static contextTypes = {
    muiTheme: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      hintText = null,
      fullWidth = false,
      inputText,
      suggestions = [],
      onChange,
    } = this.props
    const {
      muiTheme,
    } = this.context

    const style = {
      searchIcon: {
        color: muiTheme.textField.hintColor,
        verticalAlign: 'bottom',
      },
      root: {
        display: 'flex',
        flexFlow: 'row nowrap',
      },
      hint: {
        marginLeft: 32,
      },
      input: {
        marginLeft: 32,
      },
      underline: {
        bottom: 0,
        width: 'calc(100% + 48px + 20px)',
      },
      clearIconButton: {
        display: inputText.length !== 0 ? 'inherit' : 'none',
        marginRight: 20,
      },
    }

    const hintNode = (
      <span>
        <SearchIcon style={style.searchIcon} />
        {hintText}
      </span>
    )

    return (
      <Paper>
        <div style={style.root}>
          <AutoComplete
            hintText={hintNode}
            dataSource={suggestions}
            fullWidth={fullWidth}
            searchText={inputText}
            onUpdateInput={onChange}
            hintStyle={style.hint}
            inputStyle={style.input}
            underlineStyle={style.underline}
          />
          <IconButton
            style={style.clearIconButton}
            onClick={() => onChange('')}
          >
            <ClearIcon color={muiTheme.textField.hintColor} />
          </IconButton>
        </div>
      </Paper>
    )
  }
}


export default SearchTextField
