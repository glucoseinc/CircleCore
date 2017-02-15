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
  }

  /**
   * @override
   */
  render() {
    const {
      replicationLink,
      ccInfos,
    } = this.props

    const targetSlaves = replicationLink.slaves.map((slaveUuid) => ccInfos.get(slaveUuid) || slaveUuid)

    return (
      <ComponentWithIcon icon={ReplicationSlaveIcon}>
        {targetSlaves.map((slaveOrUuid, index) =>
          typeof slaveOrUuid === 'string'
            ? <span style={{backgroundColor: index % 2 ? white : grey300}}>{slaveOrUuid}</span>
            : <ReplicationSlaveLabel
                key={slaveOrUuid.uuid}
                ccInfo={slaveOrUuid}
                rootStyle={{
                  backgroundColor: index % 2 ? white : grey300,
                }}
                onCopyTouchTap={onCopyTouchTap}
              />
        )}
      </ComponentWithIcon>
    )
  }
}

export default ReplicationSlavesLabel

