import React, {Component, PropTypes} from 'react'

import {grey300, white} from 'material-ui/styles/colors'

import ComponentWithIcon from 'src/components/bases/ComponentWithIcon'
import {ReplicationSlaveIcon} from 'src/components/bases/icons'

import ReplicationSlaveLabel from 'src/components/commons/ReplicationSlaveLabel'


/**
 * ReplicationLink接続先リストラベル
 */
class ReplicationSlavesLabel extends Component {
  static propTypes = {
    replicationLink: PropTypes.object.isRequired,
    ccInfos: PropTypes.object.isRequired,
    onCopyTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      replicationLink,
      ccInfos,
      onCopyTouchTap,
    } = this.props

    const slaveCcInfos = ccInfos.filter((ccInfo) =>
      replicationLink.ccInfos.includes(ccInfo.uuid)
    )

    return (
      <ComponentWithIcon icon={ReplicationSlaveIcon}>
        {slaveCcInfos.valueSeq().map((ccInfo, index) =>
          <ReplicationSlaveLabel
            key={ccInfo.uuid}
            ccInfo={ccInfo}
            rootStyle={{
              backgroundColor: index % 2 ? white :grey300,
            }}
            onCopyTouchTap={onCopyTouchTap}
          />
        )}
      </ComponentWithIcon>
    )
  }
}

export default ReplicationSlavesLabel
