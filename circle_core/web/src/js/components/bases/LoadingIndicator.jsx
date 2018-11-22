import React from 'react'

import RefreshIndicator from 'material-ui/RefreshIndicator'
import {orange500} from 'material-ui/styles/colors'


/**
 * ロード中インジゲーター
 */
class LoadingIndicator extends React.Component {
  /**
   * @override
   */
  render() {
    const style = {
      refresh: {
        display: 'inline-block',
        position: 'relative',
      },
    }

    return (
      <RefreshIndicator
        left={20}
        top={20}
        loadingColor={orange500}
        status="loading"
        style={style.refresh}
        {...this.props}
      />
    )
  }
}

export default LoadingIndicator
