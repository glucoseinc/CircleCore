import React, {Component, PropTypes} from 'react'

import Paper from 'material-ui/Paper'
import {RadioButton, RadioButtonGroup} from 'material-ui/RadioButton'
import {grey600} from 'material-ui/styles/colors'

import ReplicationLink from 'src/models/ReplicationLink'

// import AddFlatButton from 'src/components/commons/AddFlatButton'
import CreateButton from 'src/components/commons/CreateButton'
// import DeleteIconButton from 'src/components/commons/DeleteIconButton'
import DisplayNameTextField from 'src/components/commons/DisplayNameTextField'
import MemoTextField from 'src/components/commons/MemoTextField'


/**
 * ReplicationLonk作成
 */
class ReplicationLinkNewPaper extends Component {
  static propTypes = {
    modules: PropTypes.object.isRequired,
    selectedModuleId: PropTypes.string,
    onCreateTouchTap: PropTypes.func,
  }

  state = {
    replicationLink: new ReplicationLink(),
  }

  /**
   * @override
   */
  render() {
    const {
      replicationLink,
    } = this.state
    const {
      // modules,
      // selectedModuleId,
      onCreateTouchTap,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
        padding: 8,
      },
      areaLabel: {
        padding: 8,
        color: grey600,
      },

      displayName: {
        padding: 16,
      },

      selectArea: {
        display: 'flex',
        flexFlow: 'column nowrap',
        padding: 8,
      },
      switches: {
      },
      target: {
      },
      // propertiesArea: {
      //   display: 'flex',
      //   flexFlow: 'column nowrap',
      //   padding: 8,
      // },
      // properties: {
      //   display: 'flex',
      //   flexFlow: 'column nowrap',
      //   padding: 0,
      // },
      // propertyBlock: {
      //   display: 'flex',
      //   flexFlow: 'row nowrap',
      //   alignItems: 'center',
      //   padding: 0,
      // },
      // propertyName: {
      //   padding: '0px 8px',
      //   flexGrow: 1,
      // },
      // propertyType: {
      //   padding: '0px 8px',
      //   flexGrow: 1,
      // },
      // propertyDeleteIcon: {
      //
      // propertyActionsBlock: {
      //   padding: 8,
      // },

      metadataArea: {
        display: 'flex',
        flexFlow: 'column nowrap',
        padding: 8,
      },
      memo: {
        padding: 8,
      },

      actionsArea: {
        margin: 'auto',
        padding: 16,
      },
    }

    return (
      <Paper>
        <div style={style.root}>
          <div style={style.displayName}>
            <DisplayNameTextField
              obj={replicationLink}
              floatingLabelText="共有リンク名"
              onChange={(e) => this.setState({replicationLink: replicationLink.updateDisplayName(e.target.value)})}
            />
          </div>

          <div style={style.selectArea}>
            <div style={style.switches}>
              <RadioButtonGroup
                name="targetType"
                defaultSelected="module"
              >
                <RadioButton
                  value="module"
                  label="モジュール"
                />
                <RadioButton
                  value="tag"
                  label="タグ"
                />
              </RadioButtonGroup>
            </div>
            <div style={style.target}>
            </div>
          </div>
          <div style={style.metadataArea}>
            <div style={style.areaLabel}>
              <span>メタデータ</span>
            </div>
            <div style={style.memo}>
              <MemoTextField
                obj={replicationLink}
                onChange={(e) => this.setState({replicationLink: replicationLink.updateMemo(e.target.value)})}
              />
            </div>
          </div>

          <div style={style.actionsArea}>
            <CreateButton
              disabled={replicationLink.isReadytoCreate() ? false : true}
              onTouchTap={() => onCreateTouchTap(replicationLink)}
            />
          </div>
        </div>
      </Paper>
    )
  }
}


export default ReplicationLinkNewPaper
