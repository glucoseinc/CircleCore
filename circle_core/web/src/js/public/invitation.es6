/* global CRCR_INVITATION_IS_COMPLETED:false CRCR_INVITATION_ERROR:false CRCR_INVITATION_USER:false */
import React from 'react'
import Title from 'react-title-component'
import Paper from 'material-ui/Paper'

import {colorError} from 'src/colors'
import User from 'src/models/User'
import UserEditPaper from 'src/components/UserEditPaper'


/**
 * 招待リンクからのユーザー作成
 */
export default class UserInvitation extends React.Component {
  state = {
    isCompleted: false,
    user: null,
    formValues: {},
  }

  /**
   * @override
   */
  componentWillMount() {
    // errorとuserの値をグローバル変数からひろってくる。 POSTで遷移するので...
    this.setState({
      isCompleted: CRCR_INVITATION_IS_COMPLETED ? true : false,
      error: CRCR_INVITATION_ERROR,
      user: CRCR_INVITATION_USER ? User.fromObject(CRCR_INVITATION_USER) : new User(),
    })
  }

  /**
   * @override
   */
  render() {
    if(this.state.isCompleted) {
      return this.renderCompleted()
    }

    const {
      error,
    } = this.state

    return (
      <div className="userInvitation" style={{width: 640, margin: '32px auto'}}>
        <Title render={(previousTitle) => `Invitation | ${previousTitle}`} />

        {error && <div style={{
          color: colorError,
          textAlign: 'center',
          margin: '16px',
          borderRadius: 4,
          border: '1px solid ' + colorError,
        }}>{error}</div>}

        <UserEditPaper
          isPasswordRequired={true}
          user={this.state.user}
          saveButtonLabel="登録する"
          onSaveTouchTap={::this.onSaveTouchTap}
        />

        <form ref="form" method="POST">
          {Object.keys(this.state.formValues).map((key) =>
            <input type="hidden" name={key} value={this.state.formValues[key]} key={key} />
          )}
        </form>
      </div>
    )
  }

  /**
   * ユーザー作成完了画面を表示する
   * @return {React.Component}
   */
  renderCompleted() {
    return (
      <Paper className="userInvitation is-completed" style={{width: 640, margin: '32px auto'}}>
        <Title render={(previousTitle) => `Invitation | ${previousTitle}`} />

        <div style={{padding: 24}}>
          ユーザー作成が完了しました。<br />
          CircleCoreを使うには、<a href="/">こちら</a>からログインをして下さい。
        </div>
      </Paper>
    )
  }

  /**
   * 登録ボタンが押されたら呼ばれる
   * @param {User} user
   * @param {string} currentPassword 使わない
   * @param {string} newPassword
   */
  onSaveTouchTap(user, currentPassword, newPassword) {
    console.log('onSaveTouchTap', user, currentPassword, newPassword)

    // formからsubmitさせたいので結構なクソコード. because API tokenを持ってないので。
    this.setState({
      user: user,
      formValues: {
        account: user.account,
        work: user.work,
        telephone: user.telephone,
        mailAddress: user.mailAddress,
        password: newPassword,
      },
    }, () => {
      this.refs.form.submit()
    })
  }
}