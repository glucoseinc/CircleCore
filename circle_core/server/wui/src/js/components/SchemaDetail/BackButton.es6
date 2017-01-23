import React, {Component, PropTypes} from 'react'

import RaisedButton from 'material-ui/RaisedButton'


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
        width: 160,
      },
    }

    return (
      <RaisedButton
        style={style.root}
        label="一覧へ戻る"
        primary={true}
        onTouchTap={onTouchTap}
       />
    )
  }
}

export default BackButton
