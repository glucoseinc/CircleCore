import React, {Component, PropTypes} from 'react'

import FlatButton from 'material-ui/FlatButton'


/**
 * フラットボタン
 */
class CCFlatButton extends Component {
  static propTypes = {
    label: PropTypes.string.isRequired,
    icon: PropTypes.func,
    primary: PropTypes.bool,
    secondary: PropTypes.bool,
    onTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      label,
      icon,
      primary = false,
      secondary= false,
      onTouchTap,
    } = this.props

    const style = {
      label: {
        fontWeight: 'bold',
      },
      icon: {
        width: 16,
        height: 16,
      },
    }

    const Icon = icon

    return (
      <FlatButton
        label={label}
        labelStyle={style.label}
        icon={icon ? <Icon style={style.icon}/> : null}
        primary={primary}
        secondary={secondary}
        onTouchTap={onTouchTap}
      />
    )
  }
}

export default CCFlatButton
