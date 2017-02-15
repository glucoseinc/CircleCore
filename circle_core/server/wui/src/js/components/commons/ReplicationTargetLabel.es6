import React, {Component, PropTypes} from 'react'
import {grey600} from 'material-ui/styles/colors'


/**
 * ReplicationLinkターゲットラベル
 */
class ReplicationTargetLabel extends Component {
  static propTypes = {
    messageBox: PropTypes.object.isRequired,
    rootStyle: PropTypes.object,
  }

  /**
   * @override
   */
  render() {
    const {
      messageBox,
      rootStyle = {},
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'row nowrap',
        justifyContent: 'space-between',
        width: '100%',
        padding: 8,
        fontSize: 14,
      },
      displayName: {
      },
      messageBoxes: {
      },
      messageBoxDisplayName: {
        color: grey600,
      },
    }

    const mergedRootStyle = {
      ...style.root,
      ...rootStyle,
    }

    return (
      <div style={mergedRootStyle}>
        <div style={style.displayName}>
          {messageBox.displayName || '(no name)'}
        </div>
      </div>
    )
  }
}

export default ReplicationTargetLabel
