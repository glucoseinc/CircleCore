import PropTypes from 'prop-types'
import React from 'react'

import DeleteDialog from 'src/components/commons/DeleteDialog'


/**
 * Module削除ダイアログ
 */
class ModuleDeleteDialog extends React.Component {
  static propTypes = {
    open: PropTypes.bool,
    module: PropTypes.object,
    onOkClick: PropTypes.func.isRequired,
    onCancelClick: PropTypes.func.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      open = false,
      module,
      onOkClick,
      onCancelClick,
    } = this.props

    return (
      <DeleteDialog
        obj={module}
        title="このモジュールを削除しますか？"
        onOkClick={onOkClick}
        onCancelClick={onCancelClick}
        open={open}
      />
    )
  }
}

export default ModuleDeleteDialog
