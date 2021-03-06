import PropTypes from 'prop-types'
import React from 'react'

import Paper from 'material-ui/Paper'

import ComponentWithOkCancelButton from 'src/components/bases/ComponentWithOkCancelButton'

import DisplayNameTextField from 'src/components/commons/DisplayNameTextField'


/**
 * 表示名エリア(編集状態)
 */
class DisplayNameEditingPaper extends React.Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    onUpdate: PropTypes.func,
    onOKButtonClick: PropTypes.func,
    onCancelButtonClick: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      module,
      onUpdate,
      onOKButtonClick,
      onCancelButtonClick,
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
    }

    return (
      <Paper>
        <div style={style.root}>
          <ComponentWithOkCancelButton
            okButtonLabel="保存"
            okButtonDisabled={module.isReadyToCreate() ? false : true}
            onOKButtonClick={onOKButtonClick}
            onCancelButtonClick={onCancelButtonClick}
          >
            <div style={style.contents}>
              <DisplayNameTextField
                obj={module}
                floatingLabelText="モジュール名"
                onChange={(e) => onUpdate(module.updateDisplayName(e.target.value))}
              />
            </div>
          </ComponentWithOkCancelButton>
        </div>
      </Paper>
    )
  }
}

export default DisplayNameEditingPaper
