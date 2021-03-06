import PropTypes from 'prop-types'
import React from 'react'

import FloatingActionButton from 'material-ui/FloatingActionButton'

import {AddIcon} from 'src/components/bases/icons'


/**
 * ＋アイコンのフローティングアクションボタン
 */
class AddFloatingActionButton extends React.Component {
  static propTypes = {
    onClick: PropTypes.func,
  }

  state = {
    hovered: false,
  }

  /**
   * @override
   */
  render() {
    const {
      onClick,
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
        onClick={onClick}
      >
        <AddIcon />
      </FloatingActionButton>
    )
  }
}

export default AddFloatingActionButton
