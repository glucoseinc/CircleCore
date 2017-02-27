import React, {Component, PropTypes} from 'react'

import {blue500} from 'material-ui/styles/colors'

import ReplicationMasterComponent from 'src/components/commons/ReplicationMasterComponent'
import ReplicationSlavesComponent from 'src/components/commons/ReplicationSlavesComponent'

/**
* MessageBoxコンポーネント
*/
class MessageBoxComponent extends Component {
  static propTypes = {
    messageBox: PropTypes.object.isRequired,
    ccInfos: PropTypes.object.isRequired,
    masterCcInfo: PropTypes.object.isRequired,
    backgroundColor: PropTypes.string,
  }

  /**
   * @override
   */
  render() {
    const {
      messageBox,
      ccInfos,
      masterCcInfo,
      backgroundColor = null,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
        padding: 8,
        fontSize: 14,
        lineHeight: 1,
        backgroundColor,
      },

      displayName: {
        fontWeight: 'bold',
        color: blue500,
      },

      masterCcInfo: {
        paddingTop: 8,
      },

      slaveCcInfos: {
        paddingTop: 8,
      },
      slaveCcInfo: {
        marginRight: 16,
      },
    }

    const masterCcInfoComponent = masterCcInfo.myself === false ? (
      <ReplicationMasterComponent masterCcInfo={masterCcInfo} style={style.masterCcInfo} />
    ) : null

    const slaveCcInfos = messageBox.slaveCcInfos.map((slaveCcInfoId) => ccInfos.get(slaveCcInfoId))
    const slaveCcInfosComponent = slaveCcInfos.size !== 0 ? (
      <ReplicationSlavesComponent slaveCcInfos={slaveCcInfos} style={style.slaveCcInfos} />
    ) : null

    return (
      <div style={style.root}>
        <div style={style.displayName}>
          {messageBox.displayName}
        </div>

        {masterCcInfoComponent}

        {slaveCcInfosComponent}
      </div>
    )
  }
}


export default MessageBoxComponent
