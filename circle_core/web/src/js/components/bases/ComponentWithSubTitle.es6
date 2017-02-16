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
    style: PropTypes.object,
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
      icon: {
        height: 16,
        width: 16,
      },
    }

    const Icon = icon

    return (
      <div className="componentWithSubtitle" style={this.props.style || {}}>
        <div className="componentWithSubtitle-title">
          <div className="componentWithSubtitle-titleIcon">
            {Icon ? <Icon style={style.icon} color={grey600}/> : null}
          </div>
          <h3>
            {subTitle}
          </h3>
        </div>
        <div className="componentWithSubtitle-content">
          {children}
        </div>
      </div>
    )
  }
}


export default ComponentWithSubTitle
