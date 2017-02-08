import React, {Component, PropTypes} from 'react'

import ComponentWithIconButton from 'src/components/bases/ComponentWithIconButton'
import {DeleteIcon} from 'src/components/bases/icons'

import DisplayNameTextField from 'src/components/commons/DisplayNameTextField'
import MemoTextField from 'src/components/commons/MemoTextField'
import SchemaSelectField from 'src/components/commons/SchemaSelectField'


/**
 * MessageBox編集コンポーネント
 */
class MessageBoxEditComponent extends Component {
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
        <DisplayNameTextField
          obj={messageBox}
          floatingLabelText="メッセージボックス名"
          onChange={(e) => onUpdate(messageBox.updateDisplayName(e.target.value))}
        />
        <SchemaSelectField
          selectedSchemaId={messageBox.schema}
          schemas={schemas}
          onChange={(e, i, v) => onUpdate(messageBox.updateSchema(v))}
        />
        <MemoTextField
          obj={messageBox}
          onChange={(e) => onUpdate(messageBox.updateMemo(e.target.value))}
        />
      </ComponentWithIconButton>
    )
  }
}

export default MessageBoxEditComponent
