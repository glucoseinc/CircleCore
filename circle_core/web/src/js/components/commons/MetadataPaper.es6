import React, {Component, PropTypes} from 'react'

import Paper from 'material-ui/Paper'

import MemoComponent from 'src/components/commons/MemoComponent'


/**
 * メタデータエリア
 */
class MetadataPaper extends Component {
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
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
        padding: 24,
      },
    }

    return (
      <Paper>
        <div style={style.root}>
          <MemoComponent obj={obj}/>
        </div>
      </Paper>
    )
  }
}

export default MetadataPaper
