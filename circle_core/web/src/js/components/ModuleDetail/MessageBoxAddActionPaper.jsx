import PropTypes from 'prop-types'
import React from 'react'

import Paper from 'material-ui/Paper'

import CCFlatButton from 'src/components/bases/CCFlatButton'
import {AddIcon} from 'src/components/bases/icons'


/**
 * MessageBox追加操作エリア
 */
class MessageBoxAddActionPaper extends React.Component {
  static propTypes = {
    onClick: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      onClick,
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
            onClick={onClick}
          />
        </div>
      </Paper>
    )
  }
}

export default MessageBoxAddActionPaper
