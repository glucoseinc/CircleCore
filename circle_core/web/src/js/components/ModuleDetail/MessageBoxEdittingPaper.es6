import React, {Component, PropTypes} from 'react'

import Paper from 'material-ui/Paper'

import ComponentWithOkCancelButton from 'src/components/bases/ComponentWithOkCancelButton'
import MessageBoxEditComponent from 'src/components/commons/MessageBoxEditComponent'


/**
 * MessageBoxエリア(編集状態)
 */
class MessageBoxEdittingPaper extends Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    messageBoxIndex: PropTypes.number.isRequired,
    schemas: PropTypes.object.isRequired,
    style: PropTypes.object,
    onUpdate: PropTypes.func,
    onOKButtonTouchTap: PropTypes.func,
    onCancelButtonTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      module,
      messageBoxIndex,
      schemas,
      onUpdate,
      onOKButtonTouchTap,
      onCancelButtonTouchTap,
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
          onOKButtonTouchTap={onOKButtonTouchTap}
          onCancelButtonTouchTap={onCancelButtonTouchTap}
        >
          <div style={style.contents}>
            <MessageBoxEditComponent
              messageBox={messageBox}
              schemas={schemas}
              onUpdate={(newMessageBox) => onUpdate(module.updateMessageBox(messageBoxIndex, newMessageBox))}
            />
          </div>
        </ComponentWithOkCancelButton>
      </Paper>
    )
  }
}

export default MessageBoxEdittingPaper