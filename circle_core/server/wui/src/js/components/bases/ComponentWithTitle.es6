import React, {Component, PropTypes} from 'react'


/**
 * タイトル付きコンポーネント
 */
class ComponentWithTitle extends Component {
  static propTypes = {
    title: PropTypes.string.isRequired,
    additional: PropTypes.node,
    additionalStyle: PropTypes.object,
    children: PropTypes.node,
  }

  /**
   * @override
   */
  render() {
    const {
      title,
      additional,
      additionalStyle,
      children,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
        width: '100%',
      },
      outer: {
        display: 'flex',
        flexFlow: 'row nowrap',
        justifyContent: 'space-between',
      },
      title: {
        paddingLeft: 24,
        fontWeight: 'bold',
        lineHeight: 1,
      },
      additional: {
      },
      children: {
        flexGrow: 1,
        paddingTop: 16,
      },
    }

    const mergedAdditionalStyle = {
      ...style.additional,
      ...additionalStyle,
    }

    return (
      <div style={style.root}>
        <div style={style.outer}>
          <div style={style.title}>
            {title}
          </div>
          <div style={mergedAdditionalStyle}>
            {additional}
          </div>
        </div>
        <div style={style.children}>
          {children}
        </div>
      </div>
    )
  }
}


export default ComponentWithTitle
