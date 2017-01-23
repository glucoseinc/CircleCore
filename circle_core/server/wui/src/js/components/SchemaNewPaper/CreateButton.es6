import React, {Component, PropTypes} from 'react'

import RaisedButton from 'material-ui/RaisedButton'
import ContentAdd from 'material-ui/svg-icons/content/add'


/**
 */
class CreateButton extends Component {
  static propTypes = {
    disabled: PropTypes.bool,
    onTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      disabled = false,
      onTouchTap,
    } = this.props

    const style = {
      root: {
        width: 160,
      },
      label: {
        paddingLeft: 0,
      },
      icon: {
        width: 16,
        height: 16,
      },
    }

    return (
      <RaisedButton
        style={style.root}
        label="追加する"
        labelStyle={style.label}
        icon={<ContentAdd style={style.icon} />}
        primary={true}
        disabled={disabled}
        onTouchTap={onTouchTap}
       />
    )
  }
}

export default CreateButton
