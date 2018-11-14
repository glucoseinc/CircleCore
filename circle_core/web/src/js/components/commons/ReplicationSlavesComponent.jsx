import React, {Component, PropTypes} from 'react'

import ComponentWithSubTitle from 'src/components/bases/ComponentWithSubTitle'
import {CoreIcon} from 'src/components/bases/icons'


/**
* ReplicationSlaveコンポーネント
*/
class ReplicationSlavesComponent extends Component {
  static propTypes = {
    slaveCcInfos: PropTypes.object.isRequired,
    style: PropTypes.object,
  }

  /**
   * @override
   */
  render() {
    const {
      slaveCcInfos,
      style,
    } = this.props

    const mergedStyle = {
      root: {
        ...style,
      },
    }

    return (
      <ComponentWithSubTitle subTitle="共有先" icon={CoreIcon} style={mergedStyle.root}>
        {slaveCcInfos.valueSeq().map((slaveCcInfo) =>
          <span key={slaveCcInfo.uuid} style={style.slaveCcInfo}>
            {slaveCcInfo.displayName}
          </span>
        )}
      </ComponentWithSubTitle>
    )
  }
}


export default ReplicationSlavesComponent
