import React, {Component, PropTypes} from 'react'

import OkCancelDialog from '../components/OkCancelDialog'


/**
 */
class ModuleDeleteDialog extends Component {
  static propTypes = {
    isActive: PropTypes.bool.isRequired,
    module: PropTypes.object.isRequired,
    onOkTouchTap: PropTypes.func.isRequired,
    onCancelTouchTap: PropTypes.func.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      isActive,
      module,
      onOkTouchTap,
      onCancelTouchTap,
    } = this.props

    return (
      <OkCancelDialog
        title="モジュールを削除しますか？"
        okLabel="削除"
        onOkTouchTap={() => onOkTouchTap(module)}
        cancelLabel="キャンセル"
        onCancelTouchTap={onCancelTouchTap}
        open={isActive ? true : false}
      >
        <p>{module.label}</p>
      </OkCancelDialog>
    )
  }
}

export default ModuleDeleteDialog
