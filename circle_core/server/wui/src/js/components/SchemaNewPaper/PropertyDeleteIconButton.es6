import React, {Component, PropTypes} from 'react'

import IconButton from 'material-ui/IconButton'
import ActionDelete from 'material-ui/svg-icons/action/delete'


/**
 */
class PropertyDeleteIconButton extends Component {
  static propTypes = {
    onTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      size = 24,
      iconSize = 24,
      onTouchTap,
    } = this.props

    const style = {
      root: {
        width: size,
        height: size,
        padding: (size - iconSize) / 2,
      },
      icon: {
        width: iconSize,
        height: iconSize,
      },
    }
    return (
      <IconButton
        style={style.root}
        iconStyle={style.icon}
        onTouchTap={onTouchTap}
      >
        <ActionDelete />
      </IconButton>
    )
  }
}

export default PropertyDeleteIconButton
