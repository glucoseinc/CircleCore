import PropTypes from 'prop-types'
import React from 'react'

import FlatButton from 'material-ui/FlatButton'


/**
 * Moduleボタン
 */
class ModuleButton extends React.Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    onClick: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      module,
      onClick,
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
        onClick={() => onClick(module.uuid)}
      />
    )
  }
}

export default ModuleButton
