import React, {Component, PropTypes} from 'react'

import CCRaisedButton from 'src/components/bases/CCRaisedButton'


/**
 * 一覧へ戻るボタン
 */
class BackButton extends Component {
  static propTypes = {
    onTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      onTouchTap,
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
        onTouchTap={onTouchTap}
       />
    )
  }
}

export default BackButton
