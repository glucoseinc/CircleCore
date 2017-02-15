import React, {Component, PropTypes} from 'react'

import MenuItem from 'material-ui/MenuItem'
import Paper from 'material-ui/Paper'

import ComponentWithMoreIconMenu from 'src/components/bases/ComponentWithMoreIconMenu'
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
    messageBoxes: PropTypes.object.isRequired,
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
      messageBoxes,
      // modules,
      ccInfos,
      onDisplayNameTouchTap,
      onDeleteTouchTap,
    } = this.props

    const style = {
      root: {
        padding: 24,
      },

      contents: {
        display: 'flex',
        flexFlow: 'row nowrap',
      },

      leftArea: {
        display: 'flex',
        flexFlow: 'column nowrap',
        minWidth: 232,
        maxWidth: 232,
      },
      displayName: {
        fontSize: 14,
        fontWeight: 'bold',
        cursor: 'pointer',
      },

      rightArea: {
        display: 'flex',
        flexFlow: 'column nowrap',
        flexGrow: 1,
      },
      urlSection: {
      },
      targetsSection: {
        paddingTop: 8,
      },
      coresSection: {
        paddingTop: 8,
      },
    }

    return (
      <Paper>
        <div style={style.root}>
          <ComponentWithMoreIconMenu
            menuItems={[
              <MenuItem
                primaryText="この共有リンクを削除する"
                leftIcon={<DeleteIcon />}
                onTouchTap={() => onDeleteTouchTap(replicationLink)}
              />,
            ]}
          >
            <div style={style.contents}>
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
                    messageBoxes={messageBoxes}
                  />
                </div>

                <div style={style.coresSection}>
                  <ReplicationSlavesLabel
                    replicationLink={replicationLink}
                    ccInfos={ccInfos}
                  />
                </div>

              </div>
            </div>
          </ComponentWithMoreIconMenu>
        </div>
      </Paper>
    )
  }
}

export default ReplicationLinkInfoPaper
