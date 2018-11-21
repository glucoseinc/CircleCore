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
    onOkTouchTap: PropTypes.func.isRequired,
    onCancelTouchTap: PropTypes.func.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      open,
      schema,
      onOkTouchTap,
      onCancelTouchTap,
    } = this.props

    return (
      <DeleteDialog
        obj={schema}
        title="このメッセージスキーマを削除しますか？"
        onOkTouchTap={onOkTouchTap}
        onCancelTouchTap={onCancelTouchTap}
        open={open}
      />
    )
  }
}

export default SchemaDeleteDialog
