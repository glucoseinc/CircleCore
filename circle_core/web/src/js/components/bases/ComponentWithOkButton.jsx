import PropTypes from 'prop-types'
import React from 'react'

import CCFlatButton from './CCFlatButton'


/**
 * OKボタン付きコンポーネント
 */
class ComponentWithOkButton extends React.Component {
  static propTypes = {
    okButtonLabel: PropTypes.string,
    onOKButtonClick: PropTypes.func,
    children: PropTypes.node,
  }

  /**
   * @override
   */
  render() {
    const {
      okButtonLabel = 'OK',
      onOKButtonClick,
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
            onClick={onOKButtonClick}
          />
        </div>
      </div>
    )
  }
}


export default ComponentWithOkButton
