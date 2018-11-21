import PropTypes from 'prop-types'
import React from 'react'

import FlatButton from 'material-ui/FlatButton'


/**
 * Moduleボタン
 */
class ModuleButton extends React.Component {
  static propTypes = {
    module: PropTypes.object,
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
        disabled={module ? false : true}
        label={module ? module.label : 'Loading...'}
        labelStyle={style.label}
        onClick={() => module && onClick(module.uuid)}
      />
    )
  }
}

export default ModuleButton
