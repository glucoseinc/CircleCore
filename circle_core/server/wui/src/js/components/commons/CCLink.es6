import React, {Component, PropTypes} from 'react'
import {Link} from 'react-router'

import {createPathName, createQuery} from 'src/routes'


/**
 * リンクボタン
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

    const mergedStyle = {
      textDecoration: 'none',
      ...style,
    }

    const to = {
      pathname: createPathName(url, params),
      query: createQuery(url, params),
    }

    return (
      <Link
        to={to}
        style={mergedStyle}
      >
        {children}
      </Link>
    )
  }
}

export default CCLink
