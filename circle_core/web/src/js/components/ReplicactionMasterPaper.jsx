import PropTypes from 'prop-types'
import React from 'react'

import MenuItem from 'material-ui/MenuItem'
import Paper from 'material-ui/Paper'

import {DeleteIcon} from 'src/components/bases/icons'
import MoreIconMenu from 'src/components/bases/MoreIconMenu'


/**
 * 共有マスタ
 */
export default class ReplicactionMasterPaper extends React.Component {
  static propTypes = {
    replicationMaster: PropTypes.object.isRequired,
    onDeleteTouchTap: PropTypes.func.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      replicationMaster,
      onDeleteTouchTap,
    } = this.props

    const style = {
      root: {
        padding: 24,
        position: 'relative',
      },
    }

    return (
      <Paper className="replicationMaster">
        <div style={style.root}>
          <MoreIconMenu>
            <MenuItem
              primaryText="この共有マスタを削除する"
              leftIcon={<DeleteIcon />}
              onTouchTap={() => onDeleteTouchTap(replicationMaster)}
            />
          </MoreIconMenu>

          <div>
            {replicationMaster.endpointUrl}
          </div>

        </div>
      </Paper>
    )
  }
}
