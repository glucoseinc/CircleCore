import React, {Component, PropTypes} from 'react'

import {grey500, grey900} from 'material-ui/styles/colors'
import ActionAssignment from 'material-ui/svg-icons/action/assignment'


/**
 * メモラベル
 */
class IdLabel extends Component {
  static propTypes = {
    obj: PropTypes.object.isRequired,
    onTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      obj,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'row nowrap',
        lineHeight: 1,
      },
      icon: {
        width: 16,
        height: 16,
      },
      label: {
        flexGrow: 1,
        fontSize: 14,
        paddingLeft: 8,
        paddingRight: 4,
        color: grey900,
      },
    }

    const memos = obj.memo.split('\n')

    return (
      <div
        style={style.root}
      >
        <ActionAssignment style={style.icon} color={grey500}/>
        <div style={style.label}>
          {memos.map((memo, index) => (
            <span key={index}>
              {index !== 0 && <br />}{memo}
            </span>
          ))}
        </div>
      </div>
    )
  }
}

export default IdLabel
