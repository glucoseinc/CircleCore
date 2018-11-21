import PropTypes from 'prop-types'
import React from 'react'

import {grey900} from 'material-ui/styles/colors'

import LabelWithCopyButton from 'src/containers/bases/LabelWithCopyButton'
import CCFlatButton from 'src/components/bases/CCFlatButton'


/**
 * 16文字のランダムなパスワードとして使える文字列を生成する
 * @return {str} 自動生成されたパスワード文字列
 */
function generatePassword() {
  const l = 16
  const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
  let r = ''

  for (let i = 0; i < l; i++) {
    r += chars[Math.floor(Math.random() * chars.length)]
  }
  return r
}


/**
* パスワード自動生成コンポーネント
*/
class PasswordAutoGenerateComponent extends React.Component {
  static propTypes = {
    onUpdate: PropTypes.func,
    onToggleInputMethod: PropTypes.func,
  }

  state = {
    generatedPassword: generatePassword(),
  }

  /**
   * @override
   */
  componentDidMount() {
    this.props.onUpdate(this.state.generatedPassword)
  }

  /**
   * @override
   */
  render() {
    const {
      generatedPassword,
    } = this.state
    const {
      onToggleInputMethod,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
        alignItems: 'flex-start',
      },

      inputArea: {
        paddingTop: 8,
      },
      passwordLabel: {
        fontSize: 14,
        color: grey900,
      },

      actionsArea: {
        paddingTop: 16,
      },
    }

    return (
      <div style={style.root}>
        <div style={style.inputArea}>
          <LabelWithCopyButton
            label={generatedPassword}
            labelStyle={style.passwordLabel}
            messageWhenCopying="パスワードをコピーしました"
          />
        </div>

        <div style={style.actionsArea}>
          <CCFlatButton
            label="新しいパスワードを自分で決める"
            primary={true}
            onTouchTap={onToggleInputMethod}
          />
        </div>
      </div>
    )
  }
}


export default PasswordAutoGenerateComponent
