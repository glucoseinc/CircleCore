import React, {Component, PropTypes} from 'react'

import Dialog from 'material-ui/Dialog'
import FlatButton from 'material-ui/FlatButton'


/**
 * OK/Cancelボタンを持つダイアログ
 */
class OkCancelDialog extends Component {
  static propTypes = {
    title: PropTypes.string,
    okLabel: PropTypes.string,
    okDisabled: PropTypes.bool,
    onOkTouchTap: PropTypes.func.isRequired,
    cancelLabel: PropTypes.string,
    cancelDisabled: PropTypes.bool,
    onCancelTouchTap: PropTypes.func.isRequired,
    open: PropTypes.bool.isRequired,
    children: PropTypes.node,
  }

  /**
   * @override
   */
  render() {
    const {
      title,
      okLabel = 'OK',
      okDisabled = false,
      onOkTouchTap,
      cancelLabel = 'Cancel',
      cancelDisabled = false,
      onCancelTouchTap,
      open,
      children,
    } = this.props

    const style = {
      actions: {
        paddingLeft: 16,
        paddingRight: 16,
      },
    }

    return (
      <Dialog
        title={title}
        actions={[
          <FlatButton label={cancelLabel} secondary={true} disabled={cancelDisabled} onTouchTap={onCancelTouchTap} />,
          <FlatButton label={okLabel} primary={true} disabled={okDisabled} onTouchTap={onOkTouchTap}/>,
        ]}
        actionsContainerStyle={style.actions}
        modal={true}
        open={open}
      >
        {children}
      </Dialog>
    )
  }
}

export default OkCancelDialog
