import React, {Component, PropTypes} from 'react'
import Paper from 'material-ui/Paper'
import TextField from 'material-ui/TextField'

import ReplicationLink from 'src/models/ReplicationLink'
import ComponentWithHeader from 'src/components/bases/ComponentWithHeader'
import CreateButton from 'src/components/commons/CreateButton'
import DisplayNameTextField from 'src/components/commons/DisplayNameTextField'
import MemoTextField from 'src/components/commons/MemoTextField'
import TargetSelectComponent from './TargetSelectComponent'


/**
 * ReplicationLink作成
 */
class ReplicationLinkNewPaper extends Component {
  static propTypes = {
    modules: PropTypes.object.isRequired,
    selectedModule: PropTypes.object,
    onCreateTouchTap: PropTypes.func,
  }

  state = {
    replicationLink: new ReplicationLink(),
    slaveUuids: '',
  }

  /**
   * @override
   */
  render() {
    const {
      replicationLink,
      slaveUuids,
    } = this.state
    const {
      modules,
      selectedModule,
      onCreateTouchTap,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
        padding: 24,
      },

      displayNameArea: {
      },

      slavesArea: {
      },

      selectArea: {
        paddingTop: 32,
      },

      metadataArea: {
        paddingTop: 32,
      },
      memo: {
        paddingTop: 8,
      },

      actionsArea: {
        display: 'flex',
        flexFlow: 'row nowrap',
        justifyContent: 'space-around',
        paddingTop: 40,
      },
    }

    return (
      <Paper>
        <div style={style.root}>
          <div style={style.displayNameArea}>
            <DisplayNameTextField
              obj={replicationLink}
              floatingLabelText="共有リンク名"
              onChange={(e) => this.setState({replicationLink: replicationLink.updateDisplayName(e.target.value)})}
            />
          </div>

          <div style={style.slavesArea}>
            <ComponentWithHeader headerLabel="共有先CircleCore">
              <TextField
                floatingLabelText="共有先CircleCore UUID"
                fullWidth={true}
                multiLine={true}
                rows={4}
                rowsMax={4}
                value={slaveUuids}
                onChange={(event, newValue) => this.setState({
                  slaveUuids: newValue,
                  replicationLink: replicationLink.updateSlaves(
                    newValue.split('\n').map((uuid) => uuid.trim())
                  ),
                })}
                style={{}}
                floatingLabelStyle={{}}
                textareaStyle={{}}
              />
            </ComponentWithHeader>
          </div>

          <div style={style.selectArea}>
            <ComponentWithHeader headerLabel="共有リンクタイプ">
              <TargetSelectComponent
                replicationLink={replicationLink}
                modules={modules}
                selectedModule={selectedModule}
                onUpdate={((newReplicationLink) => this.setState({replicationLink: newReplicationLink}))}
              />
            </ComponentWithHeader>
          </div>

          <div style={style.metadataArea}>
            <ComponentWithHeader headerLabel="メタデータ">
              <div style={style.memo}>
                <MemoTextField
                  obj={replicationLink}
                  onChange={(e) => this.setState({replicationLink: replicationLink.updateMemo(e.target.value)})}
                />
              </div>
            </ComponentWithHeader>
          </div>

          <div style={style.actionsArea}>
            <CreateButton
              disabled={replicationLink.isReadyToCreate() ? false : true}
              onTouchTap={() => onCreateTouchTap(replicationLink)}
            />
          </div>
        </div>
      </Paper>
    )
  }
}


export default ReplicationLinkNewPaper
