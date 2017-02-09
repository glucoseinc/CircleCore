import React, {Component, PropTypes} from 'react'

import ComponentWithTitle from 'src/components/bases/ComponentWithTitle'

import DeleteButton from 'src/components/commons/DeleteButton'

import DisplayNameEditPaper from './DisplayNameEditPaper'
import DisplayNamePaper from './DisplayNamePaper'
import MessageBoxEditPaper from './MessageBoxEditPaper'
import MessageBoxPaper from './MessageBoxPaper'
import MessageBoxAddActionPaper from './MessageBoxAddActionPaper'
import MetadataEditPaper from './MetadataEditPaper'
import MetadataPaper from './MetadataPaper'


/**
 * Module詳細コンポーネント
 */
class ModuleDetail extends Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    schemas: PropTypes.object.isRequired,
    tagSuggestions: PropTypes.array,
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
   * メッセージボックス追加ボタン押下時の動作
   */
  onMessageBoxAddTouchTap() {
    const {
      module,
    } = this.props
    this.setState({
      editingArea: ModuleDetail.editingArea.messageBox,
      editingAreaIndex: module.messageBoxes.size,
      editingModule: module.pushMessageBox(),
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
      editingAreaIndex,
      editingModule,
    } = this.state
    const {
      module,
      schemas,
      tagSuggestions = [],
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

      messageBoxAddingArea: {
        paddingTop: 40,
      },

      actionsArea: {
        paddingTop: 40,
        display: 'flex',
        flexFlow: 'row nowrap',
        justifyContent: 'center',
      },
    }

    const displayNamePaper = editingArea === ModuleDetail.editingArea.displayName ? (
      <DisplayNameEditPaper
        module={editingModule}
        onUpdate={(editingModule) => this.setState({editingModule})}
        onOKButtonTouchTap={() => this.onUpdateTouchTap()}
        onCancelButtonTouchTap={() => this.onEditCancelTouchTap()}
      />
    ) : (
      <DisplayNamePaper
        module={module}
        onEditTouchTap={() => this.onEditTouchTap(ModuleDetail.editingArea.displayName, null)}
      />
    )

    const metadataPaper = editingArea === ModuleDetail.editingArea.metadata ? (
      <MetadataEditPaper
        module={editingModule}
        tagSuggestions={tagSuggestions}
        onUpdate={(editingModule) => this.setState({editingModule})}
        onOKButtonTouchTap={() => this.onUpdateTouchTap()}
        onCancelButtonTouchTap={() => this.onEditCancelTouchTap()}
      />
    ) : (
      <MetadataPaper
        module={module}
        onEditTouchTap={() => this.onEditTouchTap(ModuleDetail.editingArea.metadata, null)}
      />
    )

    const messageBoxAddPaper = editingArea === ModuleDetail.editingArea.messageBox
    && editingAreaIndex === module.messageBoxes.size ? (
      <div style={style.messageBoxAddingArea}>
        <MessageBoxEditPaper
          module={editingModule}
          messageBoxIndex={editingAreaIndex}
          schemas={schemas}
          onUpdate={(editingModule) => this.setState({editingModule})}
          onOKButtonTouchTap={() => this.onUpdateTouchTap()}
          onCancelButtonTouchTap={() => this.onEditCancelTouchTap()}
        />
      </div>
    ) : (
      <MessageBoxAddActionPaper
        onTouchTap={() => this.onMessageBoxAddTouchTap()}
      />
    )

    return (
      <div style={style.root}>
        <div style={style.displayNameArea}>
          {displayNamePaper}
        </div>

        <div style={style.metadataArea}>
          <ComponentWithTitle title="メタデータ">
            {metadataPaper}
          </ComponentWithTitle>
        </div>

        <div style={style.messageBoxesArea}>
          <ComponentWithTitle title="メッセージボックス">
            {module.messageBoxes.valueSeq().map((messageBox, index) => {
              return editingArea === ModuleDetail.editingArea.messageBox && editingAreaIndex === index ? (
                <MessageBoxEditPaper
                  key={messageBox.uuid}
                  module={editingModule}
                  messageBoxIndex={index}
                  schemas={schemas}
                  onUpdate={(editingModule) => this.setState({editingModule})}
                  onOKButtonTouchTap={() => this.onUpdateTouchTap()}
                  onCancelButtonTouchTap={() => this.onEditCancelTouchTap()}
                />
              ) : (
                <MessageBoxPaper
                  key={messageBox.uuid}
                  module={module}
                  messageBoxIndex={index}
                  schema={schemas.get(messageBox.schema)}
                  deleteDispabled={module.messageBoxes.size <= 1}
                  onEditTouchTap={() => this.onEditTouchTap(ModuleDetail.editingArea.messageBox, index)}
                  onDeleteTouchTap={() => onMessageBoxDeleteTouchTap(index)}
                  onDownloadTouchTap={onMessageBoxDownloadTouchTap}
                />
              )
            })}
            {messageBoxAddPaper}
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
