import React, {Component, PropTypes} from 'react'

import FlatButton from 'material-ui/FlatButton'


/**
 * Moduleボタン
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
        height: 24,
        lineHeight: 1,
      },
      label: {
        padding: '0 8px',
        fontWeight: 'bold',
      },
    }

    return (
      <FlatButton
        style={style.root}
        primary={true}
        label={module.label}
        labelStyle={style.label}
        onTouchTap={() => onTouchTap(module.uuid)}
      />
    )
  }
}

export default ModuleButton
