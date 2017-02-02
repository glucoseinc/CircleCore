import React, {Component, PropTypes} from 'react'

import ComponentWithIcon from 'src/components/bases/ComponentWithIcon'
import {MemoIcon} from 'src/components/bases/icons'


/**
 * 所属ラベル
 */
class WorkLabel extends Component {
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

    const style = {
      work: {
        fontSize: 14,
        lineHeight: 1.1,
      },
    }

    return (
      <ComponentWithIcon icon={MemoIcon}>
        <div style={style.work}>
          {obj.work}
        </div>
      </ComponentWithIcon>
    )
  }
}

export default WorkLabel
