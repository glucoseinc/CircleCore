import PropTypes from 'prop-types'
import React from 'react'

import Dialog from 'material-ui/Dialog'
import FlatButton from 'material-ui/FlatButton'


/**
 * OKボタンを持つダイアログ
 */
class OkDialog extends React.Component {
  static propTypes = {
    title: PropTypes.string,
    label: PropTypes.string,
    disabled: PropTypes.bool,
    onClick: PropTypes.func.isRequired,
    open: PropTypes.bool.isRequired,
    children: PropTypes.node,
  }

  /**
   * @override
   */
  render() {
    const {
      title,
      label = 'OK',
      disabled = false,
      onClick,
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
          <FlatButton
            key="ok" label={label} primary={true} disabled={disabled} onClick={onClick}
          />,
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

export default OkDialog
