import React, {Component, PropTypes} from 'react'
import {grey500} from 'material-ui/styles/colors'

import LabelWithCopyButton from 'src/components/bases/LabelWithCopyButton'


/**
 * ReplicationLink接続先ラベル
 */
class ReplicationSlaveLabel extends Component {
  static propTypes = {
    ccInfo: PropTypes.object.isRequired,
    rootStyle: PropTypes.object,
    onCopyTouchTap: PropTypes.func,
  }


  /**
   * @override
   */
  render() {
    const {
      ccInfo,
      rootStyle = {},
      onCopyTouchTap,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
        width: '100%',
        padding: 8,
      },
      displayName: {
        fontSize: 14,
      },
      lastAccessTime: {
        fontSize: 12,
        color: grey500,
      },
      id: {
        fontSize: 12,
        color: grey500,
      },
    }

    const mergedRootStyle = {
      ...style.root,
      ...rootStyle,
    }

    return (
      <div style={mergedRootStyle}>
        <div style={style.displayName}>
          {ccInfo.displayName || '(no name)'}
        </div>
        <div style={style.lastAccessTime}>
          {ccInfo.lastAccessTime}
        </div>
        <LabelWithCopyButton
          label={ccInfo.uuid}
          labelStyle={style.id}
          onTouchTap={onCopyTouchTap}
        />
      </div>
    )
  }
}

export default ReplicationSlaveLabel
