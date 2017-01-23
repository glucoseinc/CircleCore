import React, {Component, PropTypes} from 'react'

import FlatButton from 'material-ui/FlatButton'
import ContentAdd from 'material-ui/svg-icons/content/add'


/**
 */
class PropertyAddButton extends Component {
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
      label: {
        paddingLeft: 0,
      },
      icon: {
        width: 16,
        height: 16,
      },
    }

    return (
      <FlatButton
        label="プロパティを追加する"
        labelStyle={style.label}
        icon={<ContentAdd style={style.icon} />}
        primary={true}
        onTouchTap={onTouchTap}
      />
    )
  }
}

export default PropertyAddButton
