import PropTypes from 'prop-types'
import React from 'react'
import {Link} from 'react-router-dom'

import {createPathName, createQuery, createSearchString} from 'src/routes'


/**
 * リンクボタン
 */
class CCLink extends React.Component {
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
      search: createSearchString(url, params),
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
