import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'
import {put, take} from 'redux-saga/effects'

import Dialog from 'material-ui/Dialog'
import FlatButton from 'material-ui/FlatButton'

import actions, {actionTypes} from 'src/actions'
import {store} from 'src/main'
import Invitation from 'src/models/Invitation'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'
import OkCancelDialog from 'src/components/bases/OkCancelDialog'

import CreateButton from 'src/components/commons/CreateButton'

import InvitationsTable from 'src/components/InvitationsTable'


/**
 */
class Invitations extends Component {
  static propTypes = {
    isFetching: PropTypes.bool.isRequired,
    invitations: PropTypes.object.isRequired,
    actions: PropTypes.object.isRequired,
    token: PropTypes.object.isRequired,
  }

  /**
   * @constructor
   */
  constructor(...args) {
    super(...args)

    this.state = {
      // 削除対象の招待
      deleteTargetInvitation: null,
      // 新しく作った招待
      newInvitation: null,
    }
  }

  /**
   * @override
   */
  componentWillMount() {
    this.props.actions.invitations.fetchRequest()
  }

  /**
   * @override
   */
  render() {
    if(this.props.isFetching) {
      return (
        <LoadingIndicator />
      )
    }

    const {
      invitations,
      token,
    } = this.props
    const {
      deleteTargetInvitation,
      newInvitation,
    } = this.state
    const isReadOnly = token.hasScope('user+rw') ? false : true

    return (
      <div className="page">
        {!isReadOnly &&
        <CreateButton
          label="ユーザー招待リンクを生成する"
          onTouchTap={::this.onTouchTapCreateInvitation}
        />}

        <InvitationsTable
          invitations={invitations}
          onDeleteInvitation={::this.onDeleteInvitation}
          readOnly={isReadOnly}
        />

        {deleteTargetInvitation &&
          <OkCancelDialog
            title="招待を削除しますか？"
            okLabel="削除する"
            onOkTouchTap={::this.onDeleteInvitationConfirmed}
            cancelLabel="キャンセル"
            onCancelTouchTap={() => this.setState({deleteTargetInvitation: null})}
            open={true}
          >
            <p>{`${deleteTargetInvitation.link} を削除しますか？`}</p>
          </OkCancelDialog>
        }

        {newInvitation &&
          <Dialog
            title="新しいユーザー招待リンクを作成しました。"
            actions={<FlatButton label="閉じる" primary={true} onTouchTap={::this.onConfirmNewInvitationCreated} />}
            modal={false}
            open={true}
            onRequestClose={::this.onConfirmNewInvitationCreated}
          >
            <p>{newInvitation.link}</p>
            <p>このURLを招待したいユーザーに教えてください。</p>
          </Dialog>}
      </div>
    )
  }

  /**
   * 招待リンク作成ボタンが押されたら呼ばれる. 作成してURLをユーザに提示
   */
  onTouchTapCreateInvitation() {
    const self = this

    // TODO(絶対使い方間違ってる.  create -> completeまで一貫性を持たせる方法が分からん...)
    store.runSaga(function* () {
      yield put(actions.invitations.createRequest({maxInvites: 1}))
      let {payload: {response, error}} = yield take(actionTypes.invitations.createComplete)
      if(response) {
        self.setState({newInvitation: Invitation.fromObject(response.invitation)})
      } else {
        alert(error.message)
      }
    })
  }

  /**
   * 招待リンク確認ダイアログを閉じる
   */
  onConfirmNewInvitationCreated() {
    this.setState({newInvitation: null})
  }

  /**
   * 招待リンク削除ボタンが押されたら呼ばれる。確認ダイアログを表示
   * @param {Invitation} invitation 対象の招待オブジェ
   */
  onDeleteInvitation(invitation) {
    this.setState({deleteTargetInvitation: invitation})
  }

  /**
   * 削除確認でOKされたら呼ばれる。削除する
   */
  onDeleteInvitationConfirmed() {
    this.props.actions.invitations.deleteRequest(this.state.deleteTargetInvitation)
    this.setState({deleteTargetInvitation: null})
  }
}


/**
 * [mapStateToProps description]
 * @param  {[type]} state [description]
 * @return {[type]}       [description]
 */
function mapStateToProps(state) {
  return {
    isFetching: state.asyncs.isInvitationsFetching,
    invitations: state.entities.invitations,
    token: state.auth.token,
  }
}

/**
 * [mapDispatchToProps description]
 * @param  {[type]} dispatch [description]
 * @return {[type]}          [description]
 */
function mapDispatchToProps(dispatch) {
  return {
    actions: {
      invitations: bindActionCreators(actions.invitations, dispatch),
    },
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Invitations)
