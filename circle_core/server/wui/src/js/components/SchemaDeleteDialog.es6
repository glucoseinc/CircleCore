import React, {Component, PropTypes} from 'react'

import OkCancelDialog from '../components/OkCancelDialog'


/**
 */
class SchemaDeleteDialog extends Component {
  static propTypes = {
    isActive: PropTypes.bool.isRequired,
    schema: PropTypes.object.isRequired,
    onOkTouchTap: PropTypes.func.isRequired,
    onCancelTouchTap: PropTypes.func.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      isActive,
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
        open={isActive ? true : false}
      >
        <p>{schema.label}</p>
      </OkCancelDialog>
    )
  }
}

export default SchemaDeleteDialog
