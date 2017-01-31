import React, {Component, PropTypes} from 'react'

import {grey600} from 'material-ui/styles/colors'


/**
 * サブタイトル付きコンポーネント
 */
class ComponentWithSubTitle extends Component {
  static propTypes = {
    subTitle: PropTypes.string.isRequired,
    icon: PropTypes.func,
    children: PropTypes.node,
  }

  /**
   * @override
   */
  render() {
    const {
        subTitle,
        icon,
        children,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'row nowrap',
        width: '100%',
      },

      iconArea: {
        paddingRight: 8,
        width: 16,
      },
      icon: {
        height: 16,
        width: 16,
      },

      contentArea: {
        display: 'flex',
        flexFlow: 'column nowrap',
        flexGrow: 1,
      },
      subTitle: {
        paddingTop: 2,
        fontSize: 14,
        lineHeight: 1,
        color: grey600,
      },
      children: {
        paddingTop: 8,
      },
    }

    const Icon = icon

    return (
      <div style={style.root}>
        <div style={style.iconArea}>
          {Icon ? <Icon style={style.icon} color={grey600}/> : null}
        </div>
        <div style={style.contentArea}>
          <div style={style.subTitle}>
            {subTitle}
          </div>
          <div style={style.children}>
            {children}
          </div>
        </div>
      </div>
    )
  }
}


export default ComponentWithSubTitle
