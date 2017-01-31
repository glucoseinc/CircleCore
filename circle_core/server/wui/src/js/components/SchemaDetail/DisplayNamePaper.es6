import React, {Component, PropTypes} from 'react'

import Paper from 'material-ui/Paper'
import {blue500, grey600, grey900} from 'material-ui/styles/colors'


/**
 * 表示名・UUIDエリア
 */
class DisplayNamePaper extends Component {
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
      displayName: {
        padding: 0,
        fontSize: 20,
        fontWeight: 'bold',
        color: blue500,
      },
      schemaId: {
        padding: 0,
        fontSize: 14,
        color: grey900,
      },
      schemaIdLabel: {
        padding: 0,
        fontSize: 12,
        color: grey600,
      },
    }

    return (
      <Paper>
        <div style={style.root}>
          <div style={style.displayName}>
            {schema.displayName || '(no name)'}
          </div>
          <div style={style.schemaId}>
            <span style={style.schemaIdLabel}>ID</span> {schema.uuid}
          </div>
        </div>
      </Paper>
    )
  }
}


export default DisplayNamePaper
