import React, {Component, PropTypes} from 'react'

import ComponentWithIcon from 'src/components/bases/ComponentWithIcon'
import LabelWithCopyButton from 'src/containers/bases/LabelWithCopyButton'
import {IdIcon} from 'src/components/bases/icons'


/**
 * IDラベル
 */
class IdLabel extends Component {
  static propTypes = {
    obj: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      obj,
    } = this.props

    return (
      <ComponentWithIcon icon={IdIcon}>
        <LabelWithCopyButton
          label={obj.uuid}
          messageWhenCopying="IDをコピーしました"
        />
      </ComponentWithIcon>
    )
  }
}

export default IdLabel
