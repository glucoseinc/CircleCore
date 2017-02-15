import React, {Component, PropTypes} from 'react'

import MenuItem from 'material-ui/MenuItem'
import Paper from 'material-ui/Paper'

import MoreIconMenu from 'src/components/bases/MoreIconMenu'
import {DeleteIcon} from 'src/components/bases/icons'
import UrlLabel from 'src/components/commons/UrlLabel'
import ReplicationSlavesLabel from 'src/components/commons/ReplicationSlavesLabel'
import ReplicationTargetsLabel from 'src/components/commons/ReplicationTargetsLabel'

/**
 * ReplicationLink一覧ペーパー
 */
class ReplicationLinkInfoPaper extends Component {
  static propTypes = {
    replicationLink: PropTypes.object.isRequired,
    modules: PropTypes.object.isRequired,
    ccInfos: PropTypes.object.isRequired,
    onDisplayNameTouchTap: PropTypes.func,
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
      onDisplayNameTouchTap,
      onDeleteTouchTap,
    } = this.props

    const style = {
      root: {
        position: 'relative',
        padding: '24px 64px 24px 24px',
        marginBottom: 32,
      },
      moreIconMenu: {
        position: 'absolute',
        right: 8,
        top: 16,
      },
      contents: {
        // display: 'flex',
        // flexFlow: 'row nowrap',
      },

      leftArea: {
        float: 'left',
        width: 232,
        // flexFlow: 'column nowrap',
        // minWidth: 232,
        // maxWidth: 232,
      },
      displayName: {
        fontSize: 14,
        fontWeight: 'bold',
        cursor: 'pointer',
      },
      rightArea: {
        // display: 'flex',
        // flexFlow: 'column nowrap',
        // flexGrow: 1,
        marginLeft: 240,
      },
      urlSection: {
      },
      targetsSection: {
        marginTop: 8,
      },
      coresSection: {
        marginTop: 8,
      },
    }

    return (
      <Paper className="replicationLinks-row" style={style.root}>
        <MoreIconMenu style={style.moreIconMenu}>
          <MenuItem
            primaryText="この共有リンクを削除する"
            leftIcon={<DeleteIcon />}
            onTouchTap={() => onDeleteTouchTap(replicationLink)}
          />
        </MoreIconMenu>

        <div style={style.leftArea}>
          <div style={style.displayName} onTouchTap={() => onDisplayNameTouchTap(replicationLink)}>
            {replicationLink.displayName || '(no name)'}
          </div>
        </div>

        <div style={style.rightArea}>
          <div style={style.urlSection}>
            <UrlLabel
              obj={replicationLink}
            />
          </div>

          <div style={style.targetsSection}>
            <ReplicationTargetsLabel
              replicationLink={replicationLink}
              modules={modules}
            />
          </div>

          <div style={style.coresSection}>
            <ReplicationSlavesLabel
              replicationLink={replicationLink}
              ccInfos={ccInfos}
            />
          </div>

        </div>
      </Paper>
    )
  }
}

export default ReplicationLinkInfoPaper
