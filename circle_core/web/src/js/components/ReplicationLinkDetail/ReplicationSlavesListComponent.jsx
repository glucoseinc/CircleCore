import PropTypes from 'prop-types'
import React from 'react'

import Paper from 'material-ui/Paper'
import {grey300, grey600, white} from 'material-ui/styles/colors'

import IdLabel from 'src/components/commons/IdLabel'


/**
* 接続先リストのアイテム
*/
class ReplicationSlavesListItem extends React.Component {
  static propTypes = {
    ccInfo: PropTypes.object.isRequired,
    backgroundColor: PropTypes.string,
    onIdCopyButtonClick: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      ccInfo,
      backgroundColor,
      onIdCopyButtonClick,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
        padding: '16px 24px',
        backgroundColor,
      },
      displayName: {
        fontSize: 14,
        fontWeight: 'bold',
      },
      lastAccessTime: {
        fontSize: 12,
        color: grey600,
      },
    }

    return (
      <div style={style.root}>
        <div style={style.displayName}>
          {ccInfo.displayName}
        </div>
        <div style={style.lastAccessTime}>
          最終アクセス {ccInfo.lastAccessedAt ? ccInfo.lastAccessedAt.format('LLL') : '未接続'}
        </div>
        <IdLabel
          obj={ccInfo}
          onCopyButtonClick={onIdCopyButtonClick}
        />
      </div>
    )
  }
}


/**
* 接続先リストコンポーネント
*/
class ReplicationSlavesListComponent extends React.Component {
  static propTypes = {
    replicationLink: PropTypes.object.isRequired,
    ccInfos: PropTypes.object.isRequired,
    onIdCopyButtonClick: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      replicationLink,
      ccInfos,
      onIdCopyButtonClick,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
      },
    }

    const targetSlaves = replicationLink.slaves.map((slaveUuid) => ccInfos.get(slaveUuid) || slaveUuid)

    return (
      <Paper>
        <div style={style.root}>
          {targetSlaves.map((slaveOrUuid, index) =>
            typeof slaveOrUuid === 'string' ? (
              <span style={{backgroundColor: index % 2 ? white : grey300}}>{slaveOrUuid}</span>
            ) : (
              <ReplicationSlavesListItem
                key={slaveOrUuid.uuid}
                ccInfo={slaveOrUuid}
                backgroundColor={index % 2 ? white : grey300}
                onIdCopyButtonClick={onIdCopyButtonClick}
              />
            )
          )}
        </div>
      </Paper>
    )
  }
}


export default ReplicationSlavesListComponent
