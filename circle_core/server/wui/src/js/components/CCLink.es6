import React, {Component, PropTypes} from 'react'
import {Link, formatPattern} from 'react-router'


/**
 */
class CCLink extends Component {
  static propTypes = {
    url: PropTypes.object.isRequired,
    params: PropTypes.object,
    style: PropTypes.object,
    children: PropTypes.node,
  }

  /**
   * @override
   */
  render() {
    const {
      url,
      params,
      style,
      children,
    } = this.props

    const mergedStyle = Object.assign(
      {
        textDecoration: 'none',
      },
      style
    )
    return (
      <Link
        to={formatPattern(url.fullPath, params)}
        style={mergedStyle}
      >
        {children}
      </Link>
    )
  }
}

export default CCLink
