import PropTypes from 'prop-types'
import React from 'react'

import ComponentWithIcon from 'src/components/bases/ComponentWithIcon'
import {WorkIcon} from 'src/components/bases/icons'


/**
 * 所属ラベル
 */
class WorkLabel extends React.Component {
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
      <ComponentWithIcon icon={WorkIcon}>
        <div style={style.work}>
          {obj.work}
        </div>
      </ComponentWithIcon>
    )
  }
}

export default WorkLabel
