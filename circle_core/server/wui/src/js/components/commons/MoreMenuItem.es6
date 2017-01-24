import React, {Component, PropTypes} from 'react'

import MenuItem from 'material-ui/MenuItem'


/**
 * 追加メニューアイテム
 */
class MoreMenuItem extends Component {
  static propTypes = {
    primaryText: PropTypes.string,
    leftIcon: PropTypes.func,
    disabled: PropTypes.bool,
    onTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      primaryText,
      leftIcon,
      disabled = false,
      onTouchTap,
    } = this.props

    const style = {
      lectIcon: {
        margin: '16px 4px',
        width: 16,
        height: 16,
      },
      innerDiv: {
        fontSize: 14,
        paddingLeft: 32,
        paddingRight: 0,
      },
    }

    const LectIcon = leftIcon
    return (
      <MenuItem
        primaryText={primaryText}
        leftIcon={<LectIcon style={style.lectIcon} />}
        innerDivStyle={style.innerDiv}
        disabled={disabled}
        onTouchTap={onTouchTap}
      />
    )
  }
}

export default MoreMenuItem
