import React, {Component, PropTypes} from 'react'

import ComponentWithIconButton from 'src/components/bases/ComponentWithIconButton'
import {DeleteIcon} from 'src/components/bases/icons'

import MessageBoxEditComponent from 'src/components/commons/MessageBoxEditComponent'


/**
 * 削除アイコンボタン付きMessageBox編集コンポーネント
 */
class MessageBoxEditComponentWithButton extends Component {
  static propTypes = {
    messageBox: PropTypes.object.isRequired,
    schemas: PropTypes.object.isRequired,
    deleteDisabled: PropTypes.bool,
    onUpdate: PropTypes.func,
    onDeleteTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      messageBox,
      schemas,
      deleteDisabled = false,
      onUpdate,
      onDeleteTouchTap,
    } = this.props

    const style = {
      root: {
        alignItems: 'baseline',
      },
    }

    return (
      <ComponentWithIconButton
        rootStyle={style.root}
        icon={DeleteIcon}
        iconButtonDisabled={deleteDisabled}
        onIconButtonTouchTap={onDeleteTouchTap}
      >
        <MessageBoxEditComponent
          messageBox={messageBox}
          schemas={schemas}
          onUpdate={onUpdate}
        />
      </ComponentWithIconButton>
    )
  }
}

export default MessageBoxEditComponentWithButton
