import React, {Component, PropTypes} from 'react'

import ComponentWithTitle from 'src/components/bases/ComponentWithTitle'

import DeleteButton from 'src/components/commons/DeleteButton'
import DisplayNamePaper from 'src/components/commons/DisplayNamePaper'
import MetadataPaper from 'src/components/commons/MetadataPaper'

import ReplicationTargetsTableComponent from './ReplicationTargetsTableComponent'
import ReplicationSlavesListComponent from './ReplicationSlavesListComponent'


/**
* ReplocationLink詳細コンポーネント
*/
class ReplocationLinkDetail extends Component {
  static propTypes = {
    replicationLink: PropTypes.object.isRequired,
    modules: PropTypes.object.isRequired,
    ccInfos: PropTypes.object.isRequired,
    onDeleteTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      replicationLink,
      modules,
      ccInfos,
      onDeleteTouchTap,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
      },

      displayNamePaper: {
      },

      targetsArea: {
        paddingTop: 32,
      },

      slavesArea: {
        paddingTop: 32,
      },

      metadataArea: {
        paddingTop: 32,
      },

      actionsArea: {
        paddingTop: 40,
        display: 'flex',
        flexFlow: 'row nowrap',
        justifyContent: 'center',
      },
    }

    return (
      <div style={style.root}>
        <div style={style.displayNamePaper}>
          <DisplayNamePaper
            obj={replicationLink}
            secondayType="url"
          />
        </div>

        <div style={style.targetsArea}>
          <ComponentWithTitle title="共有項目">
            <ReplicationTargetsTableComponent
              messageBoxes={replicationLink.messageBoxes}
              modules={modules}
            />
          </ComponentWithTitle>
        </div>

        <div style={style.slavesArea}>
          <ComponentWithTitle title="接続先">
            <ReplicationSlavesListComponent
              replicationLink={replicationLink}
              ccInfos={ccInfos}
            />
          </ComponentWithTitle>
        </div>

        <div style={style.metadataArea}>
          <ComponentWithTitle title="メタデータ">
            <MetadataPaper obj={replicationLink} />
          </ComponentWithTitle>
        </div>

        <div style={style.actionsArea}>
          <DeleteButton
            onTouchTap={onDeleteTouchTap}
          />
        </div>
      </div>
    )
  }
}


export default ReplocationLinkDetail
