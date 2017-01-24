import React, {Component, PropTypes} from 'react'

import OkCancelDialog from '../components/OkCancelDialog'


/**
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
      <OkCancelDialog
        title="モジュールを削除しますか？"
        okLabel="削除する"
        onOkTouchTap={() => onOkTouchTap(module)}
        cancelLabel="キャンセル"
        onCancelTouchTap={onCancelTouchTap}
        open={open}
      >
        <p>{module && module.label || ''}</p>
      </OkCancelDialog>
    )
  }
}

export default ModuleDeleteDialog
