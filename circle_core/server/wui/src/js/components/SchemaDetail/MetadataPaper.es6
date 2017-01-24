import React, {Component, PropTypes} from 'react'

import Paper from 'material-ui/Paper'
import {grey600, grey900} from 'material-ui/styles/colors'


/**
 * メタデータエリア
 */
class MetadataPaper extends Component {
  static propTypes = {
    schema: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      schema,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
        padding: 20,
      },
      memoLabel: {
        padding: 4,
        fontSize: 14,
        color: grey600,
        lineHeight: 1,
      },
      memo: {
        padding: 4,
        fontSize: 14,
        color: grey900,
        lineHeight: 1.1,
      },
    }

    return (
      <Paper>
        <div style={style.root}>
          <div style={style.memoLabel}>メモ</div>
          <div style={style.memo}>{schema.memo}</div>
        </div>
      </Paper>
    )
  }
}


export default MetadataPaper
