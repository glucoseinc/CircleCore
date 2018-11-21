import PropTypes from 'prop-types'
import React from 'react'

import DisplayNameTextField from 'src/components/commons/DisplayNameTextField'
import MemoTextField from 'src/components/commons/MemoTextField'
import SchemaSelectField from 'src/components/commons/SchemaSelectField'


/**
 * MessageBox編集コンポーネント
 */
class MessageBoxEditComponent extends React.Component {
  static propTypes = {
    messageBox: PropTypes.object.isRequired,
    schemas: PropTypes.object.isRequired,
    disabledChangeSchema: PropTypes.bool,
    onUpdate: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      messageBox,
      schemas,
      disabledChangeSchema = false,
      onUpdate,
    } = this.props

    return (
      <div>
        <DisplayNameTextField
          obj={messageBox}
          floatingLabelText="メッセージボックス名"
          onChange={(e) => onUpdate(messageBox.updateDisplayName(e.target.value))}
        />
        <SchemaSelectField
          selectedSchemaId={messageBox.schema}
          schemas={schemas}
          disabled={disabledChangeSchema}
          onChange={(e, i, v) => onUpdate(messageBox.updateSchema(v))}
        />
        <MemoTextField
          obj={messageBox}
          onChange={(e) => onUpdate(messageBox.updateMemo(e.target.value))}
        />
      </div>
    )
  }
}

export default MessageBoxEditComponent
