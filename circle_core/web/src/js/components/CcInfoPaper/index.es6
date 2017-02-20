import React, {Component, PropTypes} from 'react'

import MenuItem from 'material-ui/MenuItem'
import Paper from 'material-ui/Paper'

import {DeleteIcon} from 'src/components/bases/icons'
import MoreIconMenu from 'src/components/bases/MoreIconMenu'
import IdLabel from 'src/components/commons/IdLabel'
import WorkLabel from 'src/components/commons/WorkLabel'


/**
 * CircleCoreInfo一覧ペーパー
 */
class CcInfoPaper extends Component {
  static propTypes = {
    ccInfo: PropTypes.object.isRequired,
    onDisplayNameTouchTap: PropTypes.func,
    onDeleteTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      ccInfo,
      onDisplayNameTouchTap,
      onDeleteTouchTap,
    } = this.props

    const style = {
      root: {
        padding: 24,
        position: 'relative',
      },
      leftArea: {
        float: 'left',
        width: 232,
      },
      displayName: {
        fontSize: 14,
        fontWeight: 'bold',
        cursor: 'pointer',
      },

      rightArea: {
        marginLeft: 240,
      },
      idSection: {
      },
      workSection: {
        paddingTop: 8,
      },
    }

    return (
      <Paper>
        <div style={style.root}>
          <MoreIconMenu>
            <MenuItem
              primaryText="このCircleCoreを削除する"
              leftIcon={<DeleteIcon />}
              onTouchTap={() => onDeleteTouchTap(ccInfo)}
            />
          </MoreIconMenu>

          <div style={style.leftArea}>
            <div style={style.displayName} onTouchTap={() => onDisplayNameTouchTap(ccInfo)}>
              {ccInfo.displayName || '(no name)'}
            </div>
          </div>

          <div style={style.rightArea}>
            <div style={style.idSection}>
              <IdLabel
                obj={ccInfo}
              />
            </div>
            <div style={style.workSection}>
              <WorkLabel obj={ccInfo} />
            </div>
          </div>
        </div>
      </Paper>
    )
  }
}

export default CcInfoPaper
