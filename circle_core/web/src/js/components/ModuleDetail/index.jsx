import PropTypes from 'prop-types'
import React from 'react'

import ComponentWithTitle from 'src/components/bases/ComponentWithTitle'

import CCAPI from 'src/api'

import DeleteButton from 'src/components/commons/DeleteButton'

import DisplayNameEditablePaper from './DisplayNameEditablePaper'
import DisplayNameEdittingPaper from './DisplayNameEdittingPaper'
import MessageBoxEditablePaper from './MessageBoxEditablePaper'
import MessageBoxEdittingPaper from './MessageBoxEdittingPaper'
import MessageBoxAddActionPaper from './MessageBoxAddActionPaper'
import MetadataEditablePaper from './MetadataEditablePaper'
import MetadataEdittingPaper from './MetadataEdittingPaper'


/**
 * Module詳細コンポーネント
 */
class ModuleDetail extends React.Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    schemas: PropTypes.object.isRequired,
    ccInfos: PropTypes.object.isRequired,
    tagSuggestions: PropTypes.array,
    attributeNameSuggestions: PropTypes.array,
    attributeValueSuggestions: PropTypes.array,
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

  /**
   * @constructor
   */
  constructor(...args) {
    super(...args)

    const messageBoxesFetchingData = this.props.module.messageBoxes.reduce((_data, messageBox) => ({
      ..._data,
      [messageBox.uuid]: {
        loading: true,
        messages: null,
        schemaProperties: null,
      },
    }), {})
    this.state = {
      editingArea: null,
      editingAreaIndex: null,
      editingModule: null,
      messageBoxesFetchingData,
    }
  }

  /**
   * @override
   */
  componentDidMount() {
    this.props.module.messageBoxes.map((messageBox, index) => {
      this.fetchLatestData(messageBox)
    })
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
   * サーバから最新メッセージをとってくる
   * @param {object} messageBox
   */
  async fetchLatestData(messageBox) {
    const {messages, schema: {properties}} = await CCAPI.fetchLatestMessageBox(
      this.props.module.uuid,
      messageBox.uuid
    )

    this.setState({
      messageBoxesFetchingData: {
        ...this.state.messageBoxesFetchingData,
        [messageBox.uuid]: {
          loading: false,
          messages: messages,
          schemaProperties: properties,
        },
      },
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
      messageBoxesFetchingData,
    } = this.state
    const {
      module,
      schemas,
      ccInfos,
      tagSuggestions = [],
      attributeNameSuggestions = [],
      attributeValueSuggestions = [],
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
      <DisplayNameEdittingPaper
        module={editingModule}
        onUpdate={(editingModule) => this.setState({editingModule})}
        onOKButtonTouchTap={() => this.onUpdateTouchTap()}
        onCancelButtonTouchTap={() => this.onEditCancelTouchTap()}
      />
    ) : (
      <DisplayNameEditablePaper
        obj={module}
        secondaryType={null}
        onEditTouchTap={() => this.onEditTouchTap(ModuleDetail.editingArea.displayName, null)}
      />
    )

    const metadataPaper = editingArea === ModuleDetail.editingArea.metadata ? (
      <MetadataEdittingPaper
        module={editingModule}
        tagSuggestions={tagSuggestions}
        attributeNameSuggestions={attributeNameSuggestions}
        attributeValueSuggestions={attributeValueSuggestions}
        onUpdate={(editingModule) => this.setState({editingModule})}
        onOKButtonTouchTap={() => this.onUpdateTouchTap()}
        onCancelButtonTouchTap={() => this.onEditCancelTouchTap()}
      />
    ) : (
      <MetadataEditablePaper
        module={module}
        onEditTouchTap={() => this.onEditTouchTap(ModuleDetail.editingArea.metadata, null)}
      />
    )

    const messageBoxAddPaper = editingArea === ModuleDetail.editingArea.messageBox
      && editingAreaIndex === module.messageBoxes.size ? (
        <div style={style.messageBoxAddingArea}>
          <MessageBoxEdittingPaper
            module={editingModule}
            messageBoxIndex={editingAreaIndex}
            schemas={schemas}
            onUpdate={(editingModule) => this.setState({editingModule})}
            onOKButtonTouchTap={() => this.onUpdateTouchTap()}
            onCancelButtonTouchTap={() => this.onEditCancelTouchTap()}
          />
        </div>
      ) : !module.isReplication ? (
        <MessageBoxAddActionPaper
          onTouchTap={() => this.onMessageBoxAddTouchTap()}
        />
      ) : (
        null
      )

    const canDeleteMessageBox = module.messageBoxes.size <= 1

    return (
      <div className="moduleDetail" style={style.root}>
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
            {module.messageBoxes.map((messageBox, index) => {
              const fetchingData = messageBoxesFetchingData[messageBox.uuid]
              const disabledChangeSchema = fetchingData.loading === true || fetchingData.messages.length !== 0
              return editingArea === ModuleDetail.editingArea.messageBox && editingAreaIndex === index ? (
                <MessageBoxEdittingPaper
                  key={messageBox.uuid}
                  module={editingModule}
                  messageBoxIndex={index}
                  schemas={schemas}
                  disabledChangeSchema={disabledChangeSchema}
                  onUpdate={(editingModule) => this.setState({editingModule})}
                  onOKButtonTouchTap={() => this.onUpdateTouchTap()}
                  onCancelButtonTouchTap={() => this.onEditCancelTouchTap()}
                  style={{marginBottom: '32px'}}
                />
              ) : (
                <MessageBoxEditablePaper
                  key={messageBox.uuid}
                  module={module}
                  messageBoxIndex={index}
                  schemas={schemas}
                  ccInfos={ccInfos}
                  deleteDispabled={canDeleteMessageBox}
                  onEditTouchTap={() => this.onEditTouchTap(ModuleDetail.editingArea.messageBox, index)}
                  onDeleteTouchTap={() => onMessageBoxDeleteTouchTap(index)}
                  onDownloadTouchTap={onMessageBoxDownloadTouchTap}
                  style={{marginBottom: '32px'}}
                  fetchingData={fetchingData}
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
