import React, {Component, PropTypes} from 'react'

import Paper from 'material-ui/Paper'
import {grey600} from 'material-ui/styles/colors'

import Module from 'src/models/Module'

import AddFlatButton from 'src/components/commons/AddFlatButton'
import CreateButton from 'src/components/commons/CreateButton'
import DeleteIconButton from 'src/components/commons/DeleteIconButton'
import DisplayNameTextField from 'src/components/commons/DisplayNameTextField'
import MemoTextField from 'src/components/commons/MemoTextField'

import SchemaSelectField from './SchemaSelectField'
import TagTextField from './TagTextField'


/**
 * Module作成
 */
class ModuleNewPaper extends Component {
  static propTypes = {
    schemas: PropTypes.object.isRequired,
    tagSuggestions: PropTypes.array,
    onCreateTouchTap: PropTypes.func,
  }

  state = {
    module: new Module().pushMessageBox(),
  }

  /**
   * @override
   */
  render() {
    const {
      module,
    } = this.state
    const {
      schemas,
      tagSuggestions = [],
      onCreateTouchTap,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
        padding: 8,
      },
      areaLabel: {
        padding: 8,
        color: grey600,
      },

      displayName: {
        padding: 16,
      },

      metadataArea: {
        display: 'flex',
        flexFlow: 'column nowrap',
        padding: 8,
      },
      tags: {
        padding: 8,
      },
      tagBlock: {
        display: 'flex',
        flexFlow: 'row nowrap',
        alignItems: 'center',
        padding: 0,
      },
      tag: {
        paddingRight: 8,
      },
      tagDeleteIcon: {
        padding: '0px 8px',
      },

      tagActionsBlock: {
        padding: 8,
      },

      memo: {
        padding: 8,
      },

      messageBoxesArea: {
        display: 'flex',
        flexFlow: 'column nowrap',
        padding: 8,
      },
      messageBoxes: {
        display: 'flex',
        flexFlow: 'column nowrap',
        padding: 0,
      },
      messageBoxBlock: {
        display: 'flex',
        flexFlow: 'row nowrap',
        alignItems: 'center',
        padding: 0,
      },
      messageBoxEditPart: {
        padding: '0px 8px',
        flexGrow: 1,
      },
      messageBoxDisplayName: {
      },
      messageBoxSchema: {
      },
      messageBoxMemo: {
      },
      propertyType: {
        padding: '0px 8px',
        flexGrow: 1,
      },
      propertyDeleteIcon: {
        padding: '0px 8px',
      },

      messageBoxActionsBlock: {
        padding: 8,
      },

      actionsArea: {
        margin: 'auto',
        padding: 16,
      },
    }

    return (
      <Paper>
        <div style={style.root}>
          <div style={style.displayName}>
            <DisplayNameTextField
              obj={module}
              floatingLabelText="モジュール名"
              onChange={(e) => this.setState({module: module.updateDisplayName(e.target.value)})}
            />
          </div>

          <div style={style.metadataArea}>
            <div style={style.areaLabel}>
              <span>メタデータ</span>
            </div>
            <div style={style.tags}>
              {module.tags.valueSeq().map((tag, index) =>
                <div key={index} style={style.tagBlock}>
                  <div style={style.tag}>
                    <TagTextField
                      tag={tag}
                      suggestions={tagSuggestions}
                      onChange={
                        (searchText) => this.setState({module: module.updateTag(index, searchText)})
                      }
                    />
                  </div>
                  <div style={style.tagDeleteIcon}>
                    <DeleteIconButton
                      onTouchTap={() => this.setState({module: module.removeTag(index)})}
                    />
                  </div>
                </div>
              )}
            </div>
            <div style={style.tagActionsBlock}>
              <AddFlatButton
                label="タグを追加する"
                onTouchTap={() => this.setState({module: module.pushTag()})}
              />
            </div>
            <div style={style.memo}>
              <MemoTextField
                obj={module}
                onChange={(e) => this.setState({module: module.updateMemo(e.target.value)})}
              />
            </div>
          </div>

          <div style={style.messageBoxesArea}>
            <div style={style.areaLabel}>
              <span>メッセージボックス</span>
            </div>
            <div style={style.messageBoxes}>
              {module.messageBoxes.valueSeq().map((messageBox, index) =>
                <div key={index} style={style.messageBoxBlock}>
                  <div style={style.messageBoxEditPart}>
                    <div style={style.messageBoxDisplayName}>
                      <DisplayNameTextField
                        obj={messageBox}
                        floatingLabelText="メッセージボックス名"
                        onChange={(e) => {
                          const newMessageBox = messageBox.updateDisplayName(e.target.value)
                          this.setState({module: module.updateMessageBox(index, newMessageBox)})
                        }}
                      />
                    </div>
                    <div style={style.messageBoxSchema}>
                      <SchemaSelectField
                        selectedSchemaId={messageBox.schema}
                        schemas={schemas}
                        onChange={(e, i, v) => {
                          const newMessageBox = messageBox.updateSchema(v)
                          this.setState({module: module.updateMessageBox(index, newMessageBox)})
                        }}
                      />
                    </div>
                    <div style={style.messageBoxMemo}>
                      <MemoTextField
                        obj={messageBox}
                        onChange={(e) => {
                          const newMessageBox = messageBox.updateMemo(e.target.value)
                          this.setState({module: module.updateMessageBox(index, newMessageBox)})
                        }}
                      />
                    </div>
                  </div>
                  <DeleteIconButton
                    disabled={module.messageBoxes.size <= 1}
                    onTouchTap={() => this.setState({module: module.removeMessageBox(index)})}
                  />
                </div>
              )}
            </div>
            <div style={style.messageBoxActionsBlock}>
              <AddFlatButton
                label="メッセージボックスを追加する"
                onTouchTap={() => this.setState({module: module.pushMessageBox()})}
              />
            </div>
          </div>

          <div style={style.actionsArea}>
            <CreateButton
              disabled={module.isReadytoCreate() ? false : true}
              onTouchTap={() => onCreateTouchTap(module)}
            />
          </div>
        </div>
      </Paper>
    )
  }
}


export default ModuleNewPaper
