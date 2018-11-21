import PropTypes from 'prop-types'
import React from 'react'

import FlatButton from 'material-ui/FlatButton'


/**
 * タグボタン
 */
class TagButton extends React.Component {
  static propTypes = {
    tag: PropTypes.string.isRequired,
    onTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      tag,
      onTouchTap,
    } = this.props

    const style = {
      root: {
        height: 24,
        minWidth: 0,
        lineHeight: 1,
      },
      label: {
        padding: 0,
        fontWeight: 'bold',
      },
    }

    return (
      <FlatButton
        style={style.root}
        primary={true}
        label={tag}
        labelStyle={style.label}
        onTouchTap={() => onTouchTap(tag)}
      />
    )
  }
}

export default TagButton
