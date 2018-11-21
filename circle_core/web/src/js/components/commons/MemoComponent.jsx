import PropTypes from 'prop-types'
import React from 'react'

import ComponentWithSubTitle from 'src/components/bases/ComponentWithSubTitle'
import {MemoIcon} from 'src/components/bases/icons'


/**
 * メモコンポーネント
 */
class MemoComponent extends React.Component {
  static propTypes = {
    obj: PropTypes.object.isRequired,
    style: PropTypes.object,
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
      <ComponentWithSubTitle subTitle="メモ" icon={MemoIcon} style={this.props.style || {}}>
        <div style={style.memo}>
          {obj.memo.split('\n').map((memo, index) =>
            <span key={index}>{index !== 0 && <br />}{memo}</span>
          )}
        </div>
      </ComponentWithSubTitle>
    )
  }
}

export default MemoComponent

