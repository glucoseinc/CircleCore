import React, {Component, PropTypes} from 'react'

import MenuItem from 'material-ui/MenuItem'
import Paper from 'material-ui/Paper'
import {grey600} from 'material-ui/styles/colors'

import MoreIconMenu from 'src/components/bases/MoreIconMenu'
import {DeleteIcon} from 'src/components/bases/icons'

import IdLabel from 'src/components/commons/IdLabel'
import UrlLabel from 'src/components/commons/UrlLabel'


/**
* Invitation一覧ペーパー
*/
class InvitationInfoPaper extends Component {
  static propTypes = {
    invitation: PropTypes.object.isRequired,
    readOnly: PropTypes.bool,
    onDeleteTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      invitation,
      readOnly = true,
      onDeleteTouchTap,
    } = this.props

    const style = {
      root: {
        padding: 24,
        display: 'flex',
        flexFlow: 'row nowrap',
        alignItems: 'center',
      },

      leftArea: {
        display: 'flex',
        flexFlow: 'column nowrap',
        flexGrow: 1,
      },
      urlSection: {
      },
      idSection: {
        paddingTop: 8,
      },

      remainingInvites: {
        display: 'flex',
        flexFlow: 'column nowrap',
        fontSize: 14,
        paddingLeft: 24,
      },
      createdAt: {
        display: 'flex',
        flexFlow: 'column nowrap',
        fontSize: 14,
        paddingLeft: 24,
      },
      rightAreaLabel: {
        fontSize: 12,
        color: grey600,
      },
      moreIconMenu: {
        paddingLeft: 24,
      },
      moreIconMenuRoot: {
        position: null,
        top: null,
        right: null,
      },
    }

    const moreIconMenu = readOnly ? (
      null
    ) : (
      <MoreIconMenu style={style.moreIconMenuRoot}>
        <MenuItem
          primaryText="この招待リンクを削除する"
          leftIcon={<DeleteIcon />}
          onTouchTap={() => onDeleteTouchTap(invitation)}
        />
      </MoreIconMenu>
    )

    return (
      <Paper>
        <div style={style.root}>
          <div style={style.leftArea}>
            <div style={style.urlSection}>
              <UrlLabel
                obj={invitation}
              />
            </div>
            <div style={style.idSection}>
              <IdLabel
                obj={invitation}
              />
            </div>
          </div>

          <div style={style.remainingInvites}>
            <div style={style.rightAreaLabel}>残招待数</div>
            <div>{invitation.remainingInvites}</div>
          </div>

          <div style={style.createdAt}>
            <div style={style.rightAreaLabel}>作成日</div>
            <div>{invitation.createdAt}</div>
          </div>

          <div style={style.moreIconMenu}>
            {moreIconMenu}
          </div>
        </div>
      </Paper>
    )
  }
}


export default InvitationInfoPaper
