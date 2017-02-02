import React, {Component, PropTypes} from 'react'

import CCFlatButton from './CCFlatButton'


/**
 * OKボタン付きコンポーネント
 */
class ComponentWithOkButton extends Component {
  static propTypes = {
    okButtonLabel: PropTypes.string,
    onOKButtonTouchTap: PropTypes.func,
    children: PropTypes.node,
  }

  /**
   * @override
   */
  render() {
    const {
        okButtonLabel = 'OK',
        onOKButtonTouchTap,
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
            label={okButtonLabel}
            primary={true}
            onTouchTap={onOKButtonTouchTap}
          />
        </div>
      </div>
    )
  }
}


export default ComponentWithOkButton
