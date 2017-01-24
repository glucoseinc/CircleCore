import React, {Component, PropTypes} from 'react'

import Paper from 'material-ui/Paper'
import ActionDelete from 'material-ui/svg-icons/action/delete'

import DisplayNameLabel from '../commons/DisplayNameLabel'
import MoreMenu from '../commons/MoreMenu'
import MoreMenuItem from '../commons/MoreMenuItem'
import MessageBoxLabel from './MessageBoxLabel'
import TagButton from './TagButton'


/**
 * Moduleリストの1Module
 */
class ModuleInfoPaper extends Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    onTouchTap: PropTypes.func,
    onTagButtonTouchTap: PropTypes.func,
    onDeleteTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      module,
      onTouchTap,
      onTagButtonTouchTap,
      onDeleteTouchTap,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'row nowrap',
        padding: 8,
        cursor: 'pointer',
      },

      left: {
        display: 'flex',
        flexFlow: 'column nowrap',
        padding: 8,
        boxSizing: 'border-box',
        minWidth: 232,
        maxWidth: 232,
      },
      displayName: {
        padding: 8,
      },
      replicationMasterInfo: {
        padding: 8,
      },

      right: {
        display: 'flex',
        flexFlow: 'column nowrap',
        flexGrow: 1,
        padding: 8,
        minWidth: 0,
      },
      rightTop: {
        display: 'flex',
        flexFlow: 'row nowrap',
        padding: 0,
      },
      messageBoxes: {
        display: 'flex',
        flexFlow: 'row wrap',
        flexGrow: 1,
        padding: 0,
      },
      messageBox: {
        padding: 4,
      },
      moreButton: {
        margin: '2px 0',
        padding: 4,
        height: 24,
      },

      tags: {
        display: 'flex',
        flexFlow: 'row wrap',
        padding: 0,
      },
      tag: {
        padding: 4,
      },
    }

    return (
      <Paper>
        <div style={style.root} onTouchTap={() => onTouchTap(module)}>
          <div style={style.left}>
            <div style={style.displayName}><DisplayNameLabel obj={module} /></div>
          </div>
          <div style={style.right}>
            <div style={style.rightTop}>
              <div style={style.messageBoxes}>
                {module.messageBoxes.valueSeq().map((messageBox, index) => (
                  <div key={index} style={style.messageBox}>
                    <MessageBoxLabel
                      messageBox={messageBox}
                    />
                  </div>
                ))}
              </div>
              <div style={style.moreButton} onTouchTap={(e) => e.stopPropagation()}>
                <MoreMenu>
                  <MoreMenuItem
                    primaryText="このモジュールを削除する"
                    leftIcon={ActionDelete}
                    onTouchTap={() => onDeleteTouchTap(module)}
                  />
                </MoreMenu>
              </div>
            </div>
            <div style={style.tags} onTouchTap={(e) => e.stopPropagation()}>
              {module.tags.valueSeq().map((tag, index) => (
                <div key={index} style={style.tag}>
                  <TagButton
                    tag={tag}
                    onTouchTap={onTagButtonTouchTap}
                  />
                </div>
                ))}
            </div>
          </div>
        </div>
      </Paper>
    )
  }
}


export default ModuleInfoPaper
