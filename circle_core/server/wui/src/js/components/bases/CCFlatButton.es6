import React, {Component, PropTypes} from 'react'

import FlatButton from 'material-ui/FlatButton'


/**
 * フラットボタン
 */
class CCFlatButton extends Component {
  static propTypes = {
    icon: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      icon,
      ...other
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
        labelStyle={style.label}
        icon={icon ? <Icon style={style.icon}/> : null}
        {...other}
      />
    )
  }
}

export default CCFlatButton
