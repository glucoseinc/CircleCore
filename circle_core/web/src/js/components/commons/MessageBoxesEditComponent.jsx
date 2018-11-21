import PropTypes from 'prop-types'
import React from 'react'

import AddFlatButton from 'src/components/commons/AddFlatButton'
import MessageBoxEditComponentWithButton from 'src/components/commons/MessageBoxEditComponentWithButton'


/**
 * MessageBox編集コンポーネント
 */
class MessageBoxesEditComponent extends React.Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    schemas: PropTypes.object.isRequired,
    onUpdate: PropTypes.func,
    onDeleteClick: PropTypes.func,
    onAddClick: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      module,
      schemas,
      onUpdate,
      onDeleteClick,
      onAddClick,
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
            (<div key={index} style={style.messageBoxBlock}>
              <MessageBoxEditComponentWithButton
                messageBox={messageBox}
                schemas={schemas}
                deleteDisabled={module.messageBoxes.size <= 1}
                onUpdate={(newMessageBox) => onUpdate(index, newMessageBox)}
                onDeleteClick={() => onDeleteClick(index)}
              />
            </div>)
          )}
        </div>
        <div style={style.actionsBlock}>
          <AddFlatButton
            label="メッセージボックスを追加する"
            onClick={onAddClick}
          />
        </div>
      </div>
    )
  }
}

export default MessageBoxesEditComponent
