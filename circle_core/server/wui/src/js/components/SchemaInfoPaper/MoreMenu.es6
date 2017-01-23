import React, {Component, PropTypes} from 'react'

import IconMenu from 'material-ui/IconMenu'

import MoreButton from './MoreButton'


/**
 */
class MoreMenu extends Component {
  static propTypes = {
    children: PropTypes.node,
  }

  /**
   * @override
   */
  render() {
    const {
      children,
    } = this.props

    const style = {
      list: {
        paddingTop: 0,
        paddingBottom: 0,
      },
    }

    return (
      <IconMenu
        iconButtonElement={<MoreButton />}
        anchorOrigin={{vertical: 'bottom', horizontal: 'right'}}
        targetOrigin={{vertical: 'top', horizontal: 'right'}}
        listStyle={style.list}
      >
        {children}
      </IconMenu>
    )
  }
}

export default MoreMenu
