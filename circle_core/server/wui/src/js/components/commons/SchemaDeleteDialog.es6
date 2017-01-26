import React, {Component, PropTypes} from 'react'

import OkCancelDialog from 'src/components/bases/OkCancelDialog'


/**
 * Schema削除ダイアログ
 */
class SchemaDeleteDialog extends Component {
  static propTypes = {
    open: PropTypes.bool,
    schema: PropTypes.object,
    onOkTouchTap: PropTypes.func.isRequired,
    onCancelTouchTap: PropTypes.func.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      open = false,
      schema,
      onOkTouchTap,
      onCancelTouchTap,
    } = this.props

    return (
      <OkCancelDialog
        title="メッセージスキーマを削除しますか？"
        okLabel="削除する"
        onOkTouchTap={() => onOkTouchTap(schema)}
        cancelLabel="キャンセル"
        onCancelTouchTap={onCancelTouchTap}
        open={open}
      >
        <p>{schema && schema.label || ''}</p>
      </OkCancelDialog>
    )
  }
}

export default SchemaDeleteDialog
