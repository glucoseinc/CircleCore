// ログイン状態を見てユーザーを振り分ける
import PropTypes from 'prop-types'
import React from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'

import actions from 'src/actions'
import {OAUTH_AUTHORIZATION_URL} from 'src/Authorization'


/**
 * ログイン済ユーザ用のフレーム
 */
class UserOnlyFrame extends React.Component {
  static propTypes = {
    tokenIsValid: PropTypes.bool.isRequired,
    children: PropTypes.node,
  }
  static contextTypes = {
    router: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  componentWillMount() {
    this.guestWillTransfer(this.props, this.context.router)
  }

  /**
   * @override
   */
  componentWillUpdate(nextProps) {
    this.guestWillTransfer(nextProps, this.context.router)
  }

  /**
   * 都度呼ばれ、ユーザーのTokenが無効であれば、認証をはじめる
   * @param {object} props
   * @param {object} router
   */
  guestWillTransfer(props, router) {
    if (!props.tokenIsValid) {
      // /oauth/authorization はReact化ではないため、location.hrefを動かさないといけない
      // location.href = OAUTH_AUTHORIZATION_URL
      router.history.replace(OAUTH_AUTHORIZATION_URL)
    }
  }

  /**
   * @override
   */
  render() {
    if (!this.props.tokenIsValid) {
      return <div>ログイン中...</div>
    }
    return <div className="appContainer is-user">{this.props.children}</div>
  }
}
export const UserOnly = connect(
  (state) => {
    return {
      tokenIsValid: state.auth.tokenIsValid,
    }
  },
  (dispatch) => {
    return {
      actions: {
        auth: bindActionCreators(actions.auth, dispatch),
      },
    }
  },
)(UserOnlyFrame)


/**
 * 未ログインユーザ用のフレーム
 */
class GuestOnlyFrame extends React.Component {
  static propTypes = {
    tokenIsValid: PropTypes.bool.isRequired,
    children: PropTypes.node,
  }
  static contextTypes = {
    router: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  componentWillMount() {
    this.userWillTransfer(this.props, this.context.router)
  }

  /**
   * @override
   */
  componentWillUpdate(nextProps) {
    this.userWillTransfer(nextProps, this.context.router)
  }

  /**
   * 都度呼ばれ、ユーザーのTokenが有効になっていれば、ログイン済ユーザの領域に飛ばす
   * @param {object} props
   * @param {object} router
   */
  userWillTransfer(props, router) {
    if (props.tokenIsValid) {
      router.history.replace('/')
    }
  }

  /**
   * @override
   */
  render() {
    return <div className="appContainer is-guest">{this.props.children}</div>
  }
}
export const GuestOnly = connect(
  (state) => {
    return {
      tokenIsValid: state.auth.tokenIsValid,
    }
  },
  (dispatch) => {
    return {
      actions: {
        auth: bindActionCreators(actions.auth, dispatch),
      },
    }
  },
)(GuestOnlyFrame)
