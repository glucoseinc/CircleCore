import React, {Component, PropTypes} from 'react'

import MenuItem from 'material-ui/MenuItem'
import Paper from 'material-ui/Paper'
import {blue500} from 'material-ui/styles/colors'

import MoreIconMenu from 'src/components/bases/MoreIconMenu'
import {CheckIcon, DeleteIcon} from 'src/components/bases/icons'

import tableStyle from './tableStyle'


/**
* User一覧ペーパー
*/
class UserInfoPaper extends Component {
  static propTypes = {
    user: PropTypes.object.isRequired,
    deleteDisabled: PropTypes.bool,
    readOnly: PropTypes.bool,
    onDisplayNameTouchTap: PropTypes.func,
    onDeleteTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      user,
      deleteDisabled = true,
      readOnly = true,
      onDisplayNameTouchTap,
      onDeleteTouchTap,
    } = this.props

    const style = {
      root: {
        ...tableStyle.root,
        fontSize: 14,
      },
      displayName: {
        ...tableStyle.displayName,
        fontWeight: 'bold',
        cursor: 'pointer',
      },
      mailAddress: {
        ...tableStyle.mailAddress,
      },
      lastAccessAt: {
        ...tableStyle.lastAccessAt,
      },
      isAdmin: {
        ...tableStyle.isAdmin,
      },
      moreIconMenu: {
        ...tableStyle.moreIconMenu,
      },
    }

    const moreIconMenu = readOnly ? (
      null
    ) : (
      <MoreIconMenu>
        <MenuItem
          primaryText="このユーザーを削除する"
          leftIcon={<DeleteIcon />}
          disabled={deleteDisabled}
          onTouchTap={() => onDeleteTouchTap(user)}
        />
      </MoreIconMenu>
    )

    return (
      <Paper>
        <div style={style.root}>
          <div style={style.displayName} onTouchTap={() => onDisplayNameTouchTap(user)}>{user.displayName}</div>
          <div style={style.mailAddress}>{user.mailAddress}</div>
          <div style={style.lastAccessAt}>{user.lastAccessAt}</div>
          <div style={style.isAdmin}>{user.isAdmin ? <CheckIcon color={blue500} /> : null}</div>
          <div style={style.moreIconMenu}>{moreIconMenu}</div>
        </div>
      </Paper>
    )
  }
}


export default UserInfoPaper
