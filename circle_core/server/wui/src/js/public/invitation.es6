import React from 'react'
import Title from 'react-title-component'
import Paper from 'material-ui/Paper'

import User from 'src/models/User'
import UserEditPaper from 'src/components/UserEditPaper'


/**
 * 招待リンクからのユーザー作成
 */
export default class UserInvitation extends React.Component {
  /**
   * @constructor
   */
  constructor(...args) {
    super(...args)

    this.state = {
      user: new User(),
    }
  }

  /**
   * @override
   */
  render() {
    return (
      <Paper className="userInvitation" style={{width: 640, margin: '32px auto'}}>
        <Title render={(previousTitle) => `Invitation | ${previousTitle}`} />
        <UserEditPaper
          user={this.state.user}
          saveButtonLabel="登録する"
          onSaveTouchTap={::this.onSaveTouchTap}
        />
      </Paper>
    )
  }

  onSaveTouchTap() {
    console.log('onSaveTouchTap', arguments)
  }
}
