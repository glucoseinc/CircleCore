import PropTypes from 'prop-types'
import React from 'react'

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
class ReplicationLinkInfoPaper extends React.Component {
  static propTypes = {
    replicationLink: PropTypes.object.isRequired,
    modules: PropTypes.object.isRequired,
    ccInfos: PropTypes.object.isRequired,
    onDisplayNameClick: PropTypes.func,
    onDeleteClick: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      replicationLink,
      modules,
      ccInfos,
      onDisplayNameClick,
      onDeleteClick,
    } = this.props

    const style = {
      root: {
        position: 'relative',
        padding: '24px 64px 24px 24px',
        marginBottom: 32,
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
        <MoreIconMenu>
          <MenuItem
            primaryText="この共有リンクを削除する"
            leftIcon={<DeleteIcon />}
            onClick={() => onDeleteClick(replicationLink)}
          />
        </MoreIconMenu>

        <div style={style.leftArea}>
          <div style={style.displayName} onClick={() => onDisplayNameClick(replicationLink.uuid)}>
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
