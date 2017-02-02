import React, {Component, PropTypes} from 'react'

import Paper from 'material-ui/Paper'

import ComponentWithIcon from 'src/components/bases/ComponentWithIcon'
import ComponentWithOkCancelButton from 'src/components/bases/ComponentWithOkCancelButton'
import {IdIcon} from 'src/components/bases/icons'

import DisplayNameTextField from 'src/components/commons/DisplayNameTextField'

/**
 * 表示名・UUIDエリア(編集状態)
 */
class DisplayNameEditPaper extends Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    onDisplayNameChange: PropTypes.func,
    onOKButtonTouchTap: PropTypes.func,
    onCancelButtonTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      module,
      onDisplayNameChange,
      onOKButtonTouchTap,
      onCancelButtonTouchTap,
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
      id: {
        fontSize: 14,
        lineHeight: 1,
      },
    }

    return (
      <Paper>
        <div style={style.root}>
          <ComponentWithOkCancelButton
            okButtonLabel="保存"
            onOKButtonTouchTap={onOKButtonTouchTap}
            onCancelButtonTouchTap={onCancelButtonTouchTap}
          >
            <div style={style.contents}>
              <DisplayNameTextField
                obj={module}
                floatingLabelText="モジュール名"
                onChange={onDisplayNameChange}
              />
              <ComponentWithIcon icon={IdIcon}>
                <div style={style.id}>{module.uuid}</div>
              </ComponentWithIcon>
            </div>
          </ComponentWithOkCancelButton>
        </div>
      </Paper>
    )
  }
}

export default DisplayNameEditPaper
