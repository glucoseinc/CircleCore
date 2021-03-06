import PropTypes from 'prop-types'
import React from 'react'

import TextField from 'material-ui/TextField'

import OkCancelDialog from 'src/components/bases/OkCancelDialog'


/**
 * 共有マスター削除ダイアログ
 */
class ReplicationMasterDeleteDialog extends React.Component {
  static propTypes = {
    open: PropTypes.bool,
    replicationMaster: PropTypes.object,
    onOkClick: PropTypes.func.isRequired,
    onCancelClick: PropTypes.func.isRequired,
  }

  state = {
    inputURL: '',
  }

  /**
   * @override
   */
  render() {
    const {
      inputURL,
    } = this.state
    const {
      open,
      replicationMaster,
      onOkClick,
      onCancelClick,
    } = this.props

    if (replicationMaster === undefined || replicationMaster === null) {
      return null
    }

    return (
      <OkCancelDialog
        title="この共有マスターを削除しますか？"
        okLabel="削除する"
        okDisabled={replicationMaster.endpointUrl !== inputURL}
        onOkClick={() => onOkClick(replicationMaster)}
        cancelLabel="キャンセル"
        onCancelClick={onCancelClick}
        open={open}
      >
        <p>{replicationMaster.endpointUrl}</p>
        <TextField
          hintText="URLを入力してください"
          fullWidth={true}
          onChange={(e, v) => this.setState({inputURL: v})}
        />
      </OkCancelDialog>
    )
  }
}

export default ReplicationMasterDeleteDialog
