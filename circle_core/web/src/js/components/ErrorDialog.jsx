import PropTypes from 'prop-types'
import React from 'react'

import OkDialog from 'src/components/bases/OkDialog'


/**
* ErrorDialog
*/
class ErrorDialog extends React.Component {
  static propTypes = {
    title: PropTypes.string,
    messages: PropTypes.object,
    open: PropTypes.bool,
    onCloseRequest: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      title = 'エラー',
      messages = {},
      open = false,
      onCloseRequest,
    } = this.props

    let children
    if (messages.result === 'failure' && messages.detail !== undefined) {
      children = (
        <div>
          <div>エラーが発生しました</div>
          <div>reason : {messages.detail.reason || '(nothing)'}</div>
          <div>status : {messages.status || '(unknown)'}</div>
          <div>actionType : {messages.actionType || '(unknown)'}</div>
        </div>
      )
    } else {
      try {
        children = (
          <div>
            <div>予期しないエラーが発生しました</div>
            {Object.entries(messages).map(([key, value]) =>
              <div key={key}>{key} : {JSON.stringify(value)}</div>
            )}
          </div>
        )
      } catch (e) {
        children = (
          <div>予期しないエラーが発生しました</div>
        )
      }
    }

    return (
      <OkDialog
        title={title}
        label="閉じる"
        onClick={onCloseRequest}
        open={open}
      >
        {children}
      </OkDialog>
    )
  }
}


export default ErrorDialog
