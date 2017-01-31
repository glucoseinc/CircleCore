import React, {Component, PropTypes} from 'react'

import Paper from 'material-ui/Paper'
import {blue500} from 'material-ui/styles/colors'

import ComponentWithIcon from 'src/components/bases/ComponentWithIcon'
import ComponentWithIconButton from 'src/components/bases/ComponentWithIconButton'
import {EditIcon, IdIcon} from 'src/components/bases/icons'


/**
 * 表示名・UUIDエリア
 */
class DisplayNamePaper extends Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    onEditTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      module,
      onEditTouchTap,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'row nowrap',
        padding: 24,
      },

      contents: {
        display: 'flex',
        flexFlow: 'column nowrap',
      },
      displayName: {
        fontSize: 20,
        fontWeight: 'bold',
        color: blue500,
      },
      id: {
        fontSize: 14,
        lineHeight: 1,
      },
    }

    return (
      <Paper>
        <div style={style.root}>
          <ComponentWithIconButton
            icon={EditIcon}
            onIconButtonTouchTap={onEditTouchTap}
          >
            <div style={style.contents}>
              <div style={style.displayName}>{module.displayName || '(no name)'}</div>
              <ComponentWithIcon icon={IdIcon}>
                <div style={style.id}>{module.uuid}</div>
              </ComponentWithIcon>
            </div>
          </ComponentWithIconButton>
        </div>
      </Paper>
    )
  }
}

export default DisplayNamePaper
