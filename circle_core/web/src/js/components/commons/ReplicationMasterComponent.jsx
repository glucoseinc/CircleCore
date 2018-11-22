import PropTypes from 'prop-types'
import React from 'react'

import ComponentWithSubTitle from 'src/components/bases/ComponentWithSubTitle'
import {CoreIcon} from 'src/components/bases/icons'


/**
* 共有マスターコンポーネント
*/
class ReplicationMasterComponent extends React.Component {
  static propTypes = {
    masterCcInfo: PropTypes.object.isRequired,
    style: PropTypes.object,
  }

  /**
   * @override
   */
  render() {
    const {
      masterCcInfo,
      style,
    } = this.props

    const mergedStyle = {
      root: {
        ...style,
      },
    }

    return (
      <ComponentWithSubTitle subTitle="共有元 (共有マスター)" icon={CoreIcon} style={mergedStyle.root}>
        {!masterCcInfo.myself ? masterCcInfo.displayName : null}
      </ComponentWithSubTitle>
    )
  }
}


export default ReplicationMasterComponent
