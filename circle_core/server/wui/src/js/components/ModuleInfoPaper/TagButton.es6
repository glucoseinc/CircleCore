import React, {Component, PropTypes} from 'react'

import RaisedButton from 'material-ui/RaisedButton'
import ActionLabel from 'material-ui/svg-icons/action/label'


/**
 */
class TagButton extends Component {
  static propTypes = {
    tag: PropTypes.string.isRequired,
    onTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      tag,
      onTouchTap,
    } = this.props

    const style = {
      root: {
        height: 32,
      },
      icon: {
        width: 16,
        height: 16,
      },
    }

    return (
      <RaisedButton
        style={style.root}
        icon={<ActionLabel style={style.icon} />}
        label={tag}
        onTouchTap={() => onTouchTap(tag)}
      />
    )
  }
}

export default TagButton
