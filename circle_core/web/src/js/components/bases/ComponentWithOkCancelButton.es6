import React, {Component, PropTypes} from 'react'

import CCFlatButton from './CCFlatButton'


/**
 * OKボタン/キャンセルボタン付きコンポーネント
 */
class ComponentWithOkCancelButton extends Component {
  static propTypes = {
    okButtonLabel: PropTypes.string,
    cancelButtonLabel: PropTypes.string,
    okButtonDisabled: PropTypes.bool,
    cancelButtonDisabled: PropTypes.bool,
    onOKButtonTouchTap: PropTypes.func,
    onCancelButtonTouchTap: PropTypes.func,
    children: PropTypes.node,
  }

  /**
   * @override
   */
  render() {
    const {
        okButtonLabel = 'OK',
        cancelButtonLabel = 'キャンセル',
        okButtonDisabled = false,
        cancelButtonDisabled = false,
        onOKButtonTouchTap,
        onCancelButtonTouchTap,
        children,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
        width: '100%',
      },
      children: {
        flexGrow: 1,
      },

      actionsArea: {
        display: 'flex',
        flexFlow: 'row nowrap',
        justifyContent: 'center',
        paddingTop: 24,
      },
    }

    return (
      <div style={style.root}>
        <div style={style.children}>
          {children}
        </div>
        <div style={style.actionsArea}>
          <CCFlatButton
            label={cancelButtonLabel}
            disabled={cancelButtonDisabled}
            onTouchTap={onCancelButtonTouchTap}
          />
          <CCFlatButton
            label={okButtonLabel}
            primary={true}
            disabled={okButtonDisabled}
            onTouchTap={onOKButtonTouchTap}
          />
        </div>
      </div>
    )
  }
}


export default ComponentWithOkCancelButton
