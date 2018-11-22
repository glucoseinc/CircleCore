import PropTypes from 'prop-types'
import React from 'react'

import FlatButton from 'material-ui/FlatButton'


/**
 * フラットボタン
 */
class CCFlatButton extends React.Component {
  static propTypes = {
    style: PropTypes.object,
    labelStyle: PropTypes.object,
    icon: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      style = {},
      labelStyle = {},
      icon,
      ...other
    } = this.props

    const mergedStyle = {
      ...style,
    }

    const mergedLabelStyle = {
      fontWeight: 'bold',
      ...labelStyle,
    }

    const iconStyle = {
      width: 16,
      height: 16,
    }

    const Icon = icon

    return (
      <FlatButton
        style={mergedStyle}
        labelStyle={mergedLabelStyle}
        icon={icon ? <Icon style={iconStyle} /> : null}
        {...other}
      />
    )
  }
}

export default CCFlatButton
