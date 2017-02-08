import React, {Component, PropTypes} from 'react'

import AddFlatButton from 'src/components/commons/AddFlatButton'
import MessageBoxEditComponentWithButton from 'src/components/commons/MessageBoxEditComponentWithButton'


/**
 * MessageBox編集コンポーネント
 */
class MessageBoxesEditComponent extends Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    schemas: PropTypes.object.isRequired,
    onUpdate: PropTypes.func,
    onDeleteTouchTap: PropTypes.func,
    onAddTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      module,
      schemas,
      onUpdate,
      onDeleteTouchTap,
      onAddTouchTap,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
        width: '100%',
      },

      messageBoxes: {
        marginTop: -40,
      },
      messageBoxBlock: {
        paddingTop: 40,
      },

      actionsBlock: {
        paddingTop: 32,
      },

    }

    return (
      <div style={style.root}>
        <div style={style.messageBoxes}>
          {module.messageBoxes.valueSeq().map((messageBox, index) =>
            <div key={index} style={style.messageBoxBlock}>
              <MessageBoxEditComponentWithButton
                messageBox={messageBox}
                schemas={schemas}
                deleteDisabled={module.messageBoxes.size <= 1}
                onUpdate={(newMessageBox) => onUpdate(index, newMessageBox)}
                onDeleteTouchTap={() => onDeleteTouchTap(index)}
              />
            </div>
          )}
        </div>
        <div style={style.actionsBlock}>
          <AddFlatButton
            label="メッセージボックスを追加する"
            onTouchTap={onAddTouchTap}
          />
        </div>
      </div>
    )
  }
}

export default MessageBoxesEditComponent
