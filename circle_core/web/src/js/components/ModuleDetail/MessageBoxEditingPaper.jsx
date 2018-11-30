import PropTypes from 'prop-types'
import React from 'react'

import Paper from 'material-ui/Paper'

import ComponentWithOkCancelButton from 'src/components/bases/ComponentWithOkCancelButton'
import MessageBoxEditComponent from 'src/components/commons/MessageBoxEditComponent'


/**
 * MessageBoxエリア(編集状態)
 */
class MessageBoxEditingPaper extends React.Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    messageBoxIndex: PropTypes.number.isRequired,
    schemas: PropTypes.object.isRequired,
    disabledChangeSchema: PropTypes.bool,
    style: PropTypes.object,
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
      messageBoxIndex,
      schemas,
      disabledChangeSchema = false,
      onUpdate,
      onOKButtonClick,
      onCancelButtonClick,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'row nowrap',
        padding: 24,
        ...(this.props.style || {}),
      },

      contents: {
        display: 'flex',
        flexFlow: 'column nowrap',
      },
    }

    const messageBox = module.messageBoxes.get(messageBoxIndex)
    require('assert')(messageBox !== undefined)

    return (
      <Paper style={style.root}>
        <ComponentWithOkCancelButton
          okButtonLabel="保存"
          okButtonDisabled={module.isReadyToCreate() ? false : true}
          onOKButtonClick={onOKButtonClick}
          onCancelButtonClick={onCancelButtonClick}
        >
          <div style={style.contents}>
            <MessageBoxEditComponent
              messageBox={messageBox}
              schemas={schemas}
              disabledChangeSchema={disabledChangeSchema}
              onUpdate={(newMessageBox) => onUpdate(module.updateMessageBox(messageBoxIndex, newMessageBox))}
            />
          </div>
        </ComponentWithOkCancelButton>
      </Paper>
    )
  }
}

export default MessageBoxEditingPaper
