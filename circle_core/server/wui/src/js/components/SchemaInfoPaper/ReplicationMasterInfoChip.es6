import React, {Component, PropTypes} from 'react'

import Avatar from 'material-ui/Avatar'
import Chip from 'material-ui/Chip'
import {redA100, redA700, white} from 'material-ui/styles/colors'


/**
 * 同期Masterチップ
 */
class ReplicationMasterInfoChip extends Component {
  static propTypes = {
    replicationMaster: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      replicationMaster,
    } = this.props

    const style = {
      avatar: {
        fontSize: 14,
      },
    }

    return (
      <Chip
        backgroundColor={redA100}
      >
        <Avatar
          color={white}
          backgroundColor={redA700}
          style={style.avatar}
        >
          同期
        </Avatar>
        {replicationMaster.displayName}
      </Chip>
    )
  }
}

export default ReplicationMasterInfoChip
