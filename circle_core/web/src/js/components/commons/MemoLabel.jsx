import PropTypes from 'prop-types'
import React from 'react'

import ComponentWithIcon from 'src/components/bases/ComponentWithIcon'
import {MemoIcon} from 'src/components/bases/icons'


/**
 * メモラベル
 */
class MemoLabel extends React.Component {
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
      memo: {
        fontSize: 14,
        lineHeight: 1.1,
      },
    }

    return (
      <ComponentWithIcon icon={MemoIcon}>
        <div style={style.memo}>
          {obj.memo.split('\n').map((memo, index) =>
            <span key={index}>{index !== 0 && <br />}{memo}</span>
          )}
        </div>
      </ComponentWithIcon>
    )
  }
}

export default MemoLabel
