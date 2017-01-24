import React, {Component, PropTypes} from 'react'

import {grey300, grey900} from 'material-ui/styles/colors'
import AvNote from 'material-ui/svg-icons/av/note'


/**
 * MessageBoxのLabel
 */
class MessageBoxLabel extends Component {
  static propTypes = {
    messageBox: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      messageBox,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'row nowrap',
        alignItems: 'center',
        height: 28,
        borderRadius: 2,
        backgroundColor: grey300,
      },
      icon: {
        width: 16,
        height: 16,
        paddingLeft: 8,
      },
      label: {
        fontSize: 14,
        color: grey900,
        padding: 7,
      },
    }
    return (
      <div style={style.root}>
        <AvNote style={style.icon}/>
        <span style={style.label}>
          {messageBox.label}
        </span>
      </div>
    )
  }
}

export default MessageBoxLabel
