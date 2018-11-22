import PropTypes from 'prop-types'
import React from 'react'

import TextField from 'material-ui/TextField'

import OkCancelDialog from 'src/components/bases/OkCancelDialog'


/**
 * 削除ダイアログ
 */
class DeleteDialog extends React.Component {
  static propTypes = {
    open: PropTypes.bool,
    obj: PropTypes.object,
    primaryLabelName: PropTypes.string,
    title: PropTypes.string,
    onOkClick: PropTypes.func.isRequired,
    onCancelClick: PropTypes.func.isRequired,
  }

  state = {
    inputId: '',
  }

  /**
   * @override
   */
  render() {
    const {
      inputId,
    } = this.state
    const {
      open = false,
      obj,
      primaryLabelName = 'displayName',
      title = '削除しますか？',
      onOkClick,
      onCancelClick,
    } = this.props

    if (obj === undefined || obj === null) {
      return null
    }

    return (
      <OkCancelDialog
        title={title}
        okLabel="削除する"
        okDisabled={obj.uuid !== inputId}
        onOkClick={() => onOkClick(obj)}
        cancelLabel="キャンセル"
        onCancelClick={onCancelClick}
        open={open}
      >
        <p>{obj[primaryLabelName] || '(no name)'}</p>
        <p>{obj.uuid}</p>
        <TextField
          hintText="UUIDを入力してください"
          fullWidth={true}
          onChange={(e, v) => this.setState({inputId: v})}
        />
      </OkCancelDialog>
    )
  }
}

export default DeleteDialog
