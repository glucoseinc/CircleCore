import React, {Component, PropTypes} from 'react'

import RaisedButton from 'material-ui/RaisedButton'


/**
 * レイズドボタン
 */
class CCRaisedButton extends Component {
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
      <RaisedButton
        style={mergedStyle}
        labelStyle={mergedLabelStyle}
        icon={icon ? <Icon style={iconStyle} /> : null}
        {...other}
      />
    )
  }
}

export default CCRaisedButton
