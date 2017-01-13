import React, {Component, PropTypes} from 'react'

import Dialog from 'material-ui/Dialog'
import FlatButton from 'material-ui/FlatButton'


/**
 */
class OkCancelDialog extends Component {
  static propTypes = {
    title: PropTypes.string,
    okLabel: PropTypes.string,
    onOkTouchTap: PropTypes.func.isRequired,
    cancelLabel: PropTypes.string,
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
      okLabel,
      onOkTouchTap,
      cancelLabel,
      onCancelTouchTap,
      open,
      children,
    } = this.props

    return (
      <Dialog
        title={title}
        actions={[
          <FlatButton label={cancelLabel || 'Cancel'} secondary={true} onTouchTap={onCancelTouchTap} />,
          <FlatButton label={okLabel || 'OK'} primary={true} onTouchTap={onOkTouchTap}/>,
        ]}
        modal={true}
        open={open}
      >
        {children}
      </Dialog>
    )
  }
}

export default OkCancelDialog
