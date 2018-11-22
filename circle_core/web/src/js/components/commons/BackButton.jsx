import PropTypes from 'prop-types'
import React from 'react'

import CCRaisedButton from 'src/components/bases/CCRaisedButton'


/**
 * 一覧へ戻るボタン
 */
class BackButton extends React.Component {
  static propTypes = {
    onClick: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      onClick,
    } = this.props

    const style = {
      root: {
        minWidth: 160,
      },
    }

    return (
      <CCRaisedButton
        style={style.root}
        label="一覧へ戻る"
        primary={true}
        onClick={onClick}
      />
    )
  }
}

export default BackButton
