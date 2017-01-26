import React, {Component, PropTypes} from 'react'


/**
 * タイトル付きコンポーネント
 */
class ComponentWithTitle extends Component {
  static propTypes = {
    title: PropTypes.string.isRequired,
    children: PropTypes.node,
  }

  /**
   * @override
   */
  render() {
    const {
        title,
        children,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
        width: '100%',
      },
      title: {
        paddingLeft: 24,
        fontWeight: 'bold',
        lineHeight: 1,
      },
      children: {
        flexGrow: 1,
        paddingTop: 16,
      },
    }

    return (
      <div style={style.root}>
        <div style={style.title}>
          {title}
        </div>
        <div style={style.children}>
          {children}
        </div>
      </div>
    )
  }
}


export default ComponentWithTitle
