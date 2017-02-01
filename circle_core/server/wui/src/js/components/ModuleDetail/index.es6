import React, {Component, PropTypes} from 'react'

import ComponentWithTitle from 'src/components/bases/ComponentWithTitle'

import DeleteButton from 'src/components/commons/DeleteButton'

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
    })
  }

  /**
   * @override
   */
  render() {
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

      displayNamePaper: {
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

    return (
      <div style={style.root}>
        <div style={style.displayNamePaper}>
          <DisplayNamePaper
            module={module}
            onEditTouchTap={() => this.onEditTouchTap(ModuleDetail.editingArea.displayName, null)}
          />
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
