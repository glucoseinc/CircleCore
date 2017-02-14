import React, {Component, PropTypes} from 'react'

import DeleteDialog from 'src/components/commons/DeleteDialog'


/**
 * Module削除ダイアログ
 */
class ModuleDeleteDialog extends Component {
  static propTypes = {
    open: PropTypes.bool,
    module: PropTypes.object,
    onOkTouchTap: PropTypes.func.isRequired,
    onCancelTouchTap: PropTypes.func.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      open = false,
      module,
      onOkTouchTap,
      onCancelTouchTap,
    } = this.props

    return (
      <DeleteDialog
        obj={module}
        title="このモジュールを削除しますか？"
        onOkTouchTap={onOkTouchTap}
        onCancelTouchTap={onCancelTouchTap}
        open={open}
      />
    )
  }
}

export default ModuleDeleteDialog
