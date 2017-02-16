import React, {Component, PropTypes} from 'react'

import Paper from 'material-ui/Paper'

import CCFlatButton from 'src/components/bases/CCFlatButton'
import {AddIcon} from 'src/components/bases/icons'


/**
 * MessageBox追加操作エリア
 */
class MessageBoxAddActionPaper extends Component {
  static propTypes = {
    onTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      onTouchTap,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'row nowrap',
        padding: 24,
        justifyContent: 'center',
      },
    }

    return (
      <Paper>
        <div style={style.root}>
          <CCFlatButton
            icon={AddIcon}
            label="メッセージボックスを追加する"
            primary={true}
            onTouchTap={onTouchTap}
          />
        </div>
      </Paper>
    )
  }
}

export default MessageBoxAddActionPaper
