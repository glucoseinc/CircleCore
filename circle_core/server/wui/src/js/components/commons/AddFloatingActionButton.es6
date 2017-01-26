import React, {Component, PropTypes} from 'react'

import FloatingActionButton from 'material-ui/FloatingActionButton'

import {AddIcon} from 'src/components/bases/icons'


/**
 * ＋アイコンのフローティングアクションボタン
 */
class AddFloatingActionButton extends Component {
  static propTypes = {
    onTouchTap: PropTypes.func,
  }

  state = {
    hovered: false,
  }

  /**
   * @override
   */
  render() {
    const {
      onTouchTap,
    } = this.props

    const style = {
      position: 'fixed',
      right: 16,
      bottom: 16,
    }

    return (
      <FloatingActionButton
        style={style}
        secondary={true}
        onTouchTap={onTouchTap}
      >
        <AddIcon />
      </FloatingActionButton>
    )
  }
}

export default AddFloatingActionButton
