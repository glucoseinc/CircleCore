import React, {Component, PropTypes} from 'react'

import FlatButton from 'material-ui/FlatButton'
import ContentAdd from 'material-ui/svg-icons/content/add'


/**
 */
class AddFlatButton extends Component {
  static propTypes = {
    label: PropTypes.string,
    onTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      label = '追加する',
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
        label={label}
        labelStyle={style.label}
        icon={<ContentAdd style={style.icon} />}
        primary={true}
        onTouchTap={onTouchTap}
      />
    )
  }
}

export default AddFlatButton
