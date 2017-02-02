import React, {Component, PropTypes} from 'react'

import ComponentWithTitle from 'src/components/bases/ComponentWithTitle'

import DeleteButton from 'src/components/commons/DeleteButton'

import DisplayNameEditPaper from './DisplayNameEditPaper'
import DisplayNamePaper from './DisplayNamePaper'
import MessageBoxPaper from './MessageBoxPaper'
import MessageBoxAddActionPaper from './MessageBoxAddActionPaper'
import MetadataPaper from './MetadataPaper'


/**
 * Module詳細コンポーネント
 */
class ModuleDetail extends Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    schemas: PropTypes.object.isRequired,
    onUpdateTouchTap: PropTypes.func,
    onMessageBoxDeleteTouchTap: PropTypes.func,
    onMessageBoxDownloadTouchTap: PropTypes.func,
    onDeleteTouchTap: PropTypes.func,
  }

  static editingArea = {
    displayName: 'DISPLAY_NAME',
    metadata: 'METADATA',
    messageBox: 'MESSAGE_BOX',
  }

  state = {
    editingArea: null,
    editingAreaIndex: null,
    editingModule: null,
  }

  /**
   * 編集ボタン押下時の動作
   * @param {string} editingArea
   * @param {number} editingAreaIndex
   */
  onEditTouchTap(editingArea, editingAreaIndex) {
    this.setState({
      editingArea,
      editingAreaIndex,
      editingModule: this.props.module,
    })
  }

  /**
   * 保存ボタン押下時の動作
   */
  onUpdateTouchTap() {
    this.props.onUpdateTouchTap(this.state.editingModule)
    // TODO: 保存失敗時には編集中の状態を復元したい
    this.setState({
      editingArea: null,
      editingAreaIndex: null,
      editingModule: null,
    })
  }


  /**
   * 編集キャンセルボタン押下時の動作
   */
  onEditCancelTouchTap() {
    this.setState({
      editingArea: null,
      editingAreaIndex: null,
      editingModule: null,
    })
  }

  /**
   * @override
   */
  render() {
    const {
      editingArea,
      editingModule,
    } = this.state
    const {
      module,
      schemas,
      onMessageBoxDeleteTouchTap,
      onMessageBoxDownloadTouchTap,
      onDeleteTouchTap,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
      },

      displayNameArea: {
      },

      metadataArea: {
        paddingTop: 32,
      },

      messageBoxesArea: {
        paddingTop: 32,
      },
      messageBoxAddButton: {
        height: 16,
        lineHeight: 1,
      },
      messageBoxAddButtonLabel: {
        display: 'inline-block',
        padding: 0,
        fontWeight: 'bold',
      },

      actionsArea: {
        paddingTop: 40,
        display: 'flex',
        flexFlow: 'row nowrap',
        justifyContent: 'center',
      },
    }

    const displayNameArea = editingArea == ModuleDetail.editingArea.displayName ? (
      <DisplayNameEditPaper
        module={editingModule}
        onDisplayNameChange={(e) => this.setState({editingModule: editingModule.updateDisplayName(e.target.value)})}
        onOKButtonTouchTap={() => this.onUpdateTouchTap()}
        onCancelButtonTouchTap={() => this.onEditCancelTouchTap()}
      />
    ) : (
      <DisplayNamePaper
        module={module}
        onEditTouchTap={() => this.onEditTouchTap(ModuleDetail.editingArea.displayName, null)}
      />
    )

    return (
      <div style={style.root}>
        <div style={style.displayNameArea}>
          {displayNameArea}
        </div>

        <div style={style.metadataArea}>
          <ComponentWithTitle title="メタデータ">
            <MetadataPaper
              module={module}
              onEditTouchTap={() => this.onEditTouchTap(ModuleDetail.editingArea.metadata, null)}
            />
          </ComponentWithTitle>
        </div>

        <div style={style.messageBoxesArea}>
          <ComponentWithTitle title="メッセージボックス">
            {module.messageBoxes.valueSeq().map((messageBox, index) =>
              <MessageBoxPaper
                key={index}
                module={module}
                messageBox={messageBox}
                schema={schemas.get(messageBox.schema)}
                onEditTouchTap={() => this.onEditTouchTap(ModuleDetail.editingArea.messageBox, index)}
                onDeleteTouchTap={() => onMessageBoxDeleteTouchTap(messageBox)}
                onDownloadTouchTap={onMessageBoxDownloadTouchTap}
              />
            )}
            <MessageBoxAddActionPaper
              onTouchTap={() => console.log('メッセージボックスを追加する')}
            />
          </ComponentWithTitle>
        </div>

        <div style={style.actionsArea}>
          <DeleteButton
            label="このモジュールを削除する"
            onTouchTap={onDeleteTouchTap}
          />
        </div>
      </div>
    )
  }
}


export default ModuleDetail
