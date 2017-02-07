import React, {Component, PropTypes} from 'react'

import ComponentWithIcon from 'src/components/bases/ComponentWithIcon'
import LabelWithCopyButton from 'src/components/bases/LabelWithCopyButton'
import {IdIcon} from 'src/components/bases/icons'


/**
 * IDラベル
 */
class IdLabel extends Component {
  static propTypes = {
    obj: PropTypes.object.isRequired,
    onCopyButtonTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      obj,
      onCopyButtonTouchTap,
    } = this.props

    return (
      <ComponentWithIcon icon={IdIcon}>
        <LabelWithCopyButton
          label={obj.uuid}
          onTouchTap={onCopyButtonTouchTap}
        />
      </ComponentWithIcon>
    )
  }
}

export default IdLabel
