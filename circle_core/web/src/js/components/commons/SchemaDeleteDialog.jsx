import PropTypes from 'prop-types'
import React from 'react'

import DeleteDialog from 'src/components/commons/DeleteDialog'


/**
 * Schema削除ダイアログ
 */
class SchemaDeleteDialog extends React.Component {
  static propTypes = {
    open: PropTypes.bool,
    schema: PropTypes.object,
    onOkClick: PropTypes.func.isRequired,
    onCancelClick: PropTypes.func.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      open,
      schema,
      onOkClick,
      onCancelClick,
    } = this.props

    return (
      <DeleteDialog
        obj={schema}
        title="このメッセージスキーマを削除しますか？"
        onOkClick={onOkClick}
        onCancelClick={onCancelClick}
        open={open}
      />
    )
  }
}

export default SchemaDeleteDialog
