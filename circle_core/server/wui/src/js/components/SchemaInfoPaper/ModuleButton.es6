import React, {Component, PropTypes} from 'react'

import RaisedButton from 'material-ui/RaisedButton'
import ActionSettingsInputComponent from 'material-ui/svg-icons/action/settings-input-component'


/**
 */
class ModuleButton extends Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    onTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      module,
      onTouchTap,
    } = this.props

    const style = {
      root: {
        height: 32,
      },
      icon: {
        width: 16,
        height: 16,
      },
    }

    return (
      <RaisedButton
        style={style.root}
        icon={<ActionSettingsInputComponent style={style.icon} />}
        label={module.label}
        onTouchTap={() => onTouchTap(module.uuid)}
      />
    )
  }
}

export default ModuleButton
