import PropTypes from 'prop-types'
import React from 'react'
import {grey500} from 'material-ui/styles/colors'

import LabelWithCopyButton from 'src/containers/bases/LabelWithCopyButton'


/**
 * ReplicationLink接続先ラベル.
 */
class ReplicationSlaveLabel extends React.Component {
  static propTypes = {
    ccInfo: PropTypes.object.isRequired,
    rootStyle: PropTypes.object,
  }

  /**
   * @override
   */
  render() {
    const {
      ccInfo,
    } = this.props

    const style = {
      root: {
        // display: 'flex',
        // flexFlow: 'column nowrap',
        // width: '100%',
        // padding: 8,
        ...(this.props.rootStyle || {}),
      },
      displayName: {
        fontSize: 14,
      },
      lastAccessedAt: {
        fontSize: 12,
        color: grey500,
      },
      id: {
        fontSize: 12,
        color: grey500,
      },
    }

    return (
      <div style={style.root}>
        <div style={style.displayName}>
          {ccInfo.isSynced()
            ? (ccInfo.displayName || '(no name)')
            : <span className="not-synced">(未接続)</span>}
        </div>
        {ccInfo.isSynced() &&
          <div style={style.lastAccessedAt}>
            {ccInfo.lastAccessedAt.format('LLL')}
          </div>
        }
        <LabelWithCopyButton
          label={ccInfo.uuid}
          labelStyle={style.id}
          messageWhenCopying="IDをコピーしました"
        />
      </div>
    )
  }
}

export default ReplicationSlaveLabel
