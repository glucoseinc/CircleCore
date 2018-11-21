import PropTypes from 'prop-types'
import React from 'react'

import MenuItem from 'material-ui/MenuItem'
import Paper from 'material-ui/Paper'

import {DeleteIcon} from 'src/components/bases/icons'
import MoreIconMenu from 'src/components/bases/MoreIconMenu'

import ModuleAttributesLabel from './ModuleAttributesLabel'
import MessageBoxesLabel from './MessageBoxesLabel'
import TagButtons from './TagButtons'


/**
 * Module一覧ペーパー
 */
class ModuleInfoPaper extends React.Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    ccInfos: PropTypes.object.isRequired,
    onDisplayNameTouchTap: PropTypes.func,
    onTagButtonTouchTap: PropTypes.func,
    onDeleteTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      module,
      ccInfos,
      onDisplayNameTouchTap,
      onTagButtonTouchTap,
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
      messageBoxesSection: {
        marginRight: 16,
      },
      tagsSection: {
        paddingTop: 8,
      },
      attributesSection: {
        paddingTop: 8,
      },
    }

    return (
      <Paper>
        <div style={style.root}>
          <MoreIconMenu>
            <MenuItem
              primaryText="このモジュールを削除する"
              leftIcon={<DeleteIcon />}
              onTouchTap={() => onDeleteTouchTap(module)}
            />
          </MoreIconMenu>

          <div style={style.leftArea}>
            <div style={style.displayName} onTouchTap={() => onDisplayNameTouchTap(module)}>
              {module.displayName || '(no name)'}
            </div>
          </div>

          <div style={style.rightArea}>
            <div style={style.messageBoxesSection}>
              <MessageBoxesLabel
                module={module}
                ccInfos={ccInfos}
              />
            </div>
            <div style={style.tagsSection}>
              <TagButtons
                module={module}
                onTouchTap={onTagButtonTouchTap}
              />
            </div>
            <div style={style.attributesSection}>
              <ModuleAttributesLabel
                module={module}
              />
            </div>
          </div>
        </div>
      </Paper>
    )
  }
}


export default ModuleInfoPaper
