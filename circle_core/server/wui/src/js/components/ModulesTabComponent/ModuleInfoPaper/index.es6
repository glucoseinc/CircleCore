import React, {Component, PropTypes} from 'react'

import MenuItem from 'material-ui/MenuItem'
import Paper from 'material-ui/Paper'

import ComponentWithMoreIconMenu from 'src/components/bases/ComponentWithMoreIconMenu'
import {DeleteIcon} from 'src/components/bases/icons'

import IdLabel from 'src/components/commons/IdLabel'

import MessageBoxesLabel from './MessageBoxesLabel'
import TagButtons from './TagButtons'


/**
 * Module一覧ペーパー
 */
class ModuleInfoPaper extends Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    onDisplayNameTouchTap: PropTypes.func,
    onIdCopyButtonTouchTap: PropTypes.func,
    onTagButtonTouchTap: PropTypes.func,
    onDeleteTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      module,
      onDisplayNameTouchTap,
      onIdCopyButtonTouchTap,
      onTagButtonTouchTap,
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
      idSection: {
      },
      messageBoxesSection: {
        paddingTop: 8,
      },
      tagsSection: {
        paddingTop: 8,
      },
    }

    return (
      <Paper>
        <div style={style.root}>
          <ComponentWithMoreIconMenu
            menuItems={[
              <MenuItem
                primaryText="このモジュールを削除する"
                leftIcon={<DeleteIcon />}
                onTouchTap={() => onDeleteTouchTap(module)}
              />,
            ]}
          >
            <div style={style.contents}>
              <div style={style.leftArea}>
                <div style={style.displayName} onTouchTap={() => onDisplayNameTouchTap(module)}>
                  {module.displayName || '(no name)'}
                </div>
              </div>

              <div style={style.rightArea}>
                <div style={style.idSection}>
                  <IdLabel
                    obj={module}
                    onCopyButtonTouchTap={onIdCopyButtonTouchTap}
                  />
                </div>
                <div style={style.messageBoxesSection}>
                  <MessageBoxesLabel module={module}/>
                </div>
                <div style={style.tagsSection}>
                  <TagButtons
                    module={module}
                    onTouchTap={onTagButtonTouchTap}
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


export default ModuleInfoPaper
