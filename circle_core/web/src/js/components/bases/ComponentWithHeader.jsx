import PropTypes from 'prop-types'
import React from 'react'

import {grey600} from 'material-ui/styles/colors'


/**
 * ヘッダ付きコンポーネント
 */
class ComponentWithHeader extends React.Component {
  static propTypes = {
    headerLabel: PropTypes.string.isRequired,
    children: PropTypes.node,
  }

  /**
   * @override
   */
  render() {
    const {
      headerLabel,
      children,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
        width: '100%',
      },
      headerLabel: {
        fontSize: 14,
        fontWeight: 'bold',
        lineHeight: 1,
        color: grey600,
      },
      children: {
        flexGrow: 1,
      },
    }

    return (
      <div style={style.root}>
        <div style={style.headerLabel}>
          {headerLabel}
        </div>
        <div style={style.children}>
          {children}
        </div>
      </div>
    )
  }
}


export default ComponentWithHeader
