import React, {Component, PropTypes} from 'react'

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
        {targetSlaves.map((slave, index) =>
          <ReplicationSlaveLabel
            key={slave.uuid}
            ccInfo={slave}
            rootStyle={{
              marginTop: index > 0 ? 8 : 0,
            }}
          />
        )}
      </ComponentWithIcon>
    )
  }
}

export default ReplicationSlavesLabel

