import React, {Component, PropTypes} from 'react'

import MenuItem from 'material-ui/MenuItem'
import Paper from 'material-ui/Paper'

import CCFlatButton from 'src/components/bases/CCFlatButton'
import ComponentWithMoreIconMenu from 'src/components/bases/ComponentWithMoreIconMenu'
import ComponentWithSubTitle from 'src/components/bases/ComponentWithSubTitle'
import {DeleteIcon, DownloadIcon, EditIcon, SchemaIcon} from 'src/components/bases/icons'

import SchemaPropertiesLabel from 'src/components/commons/SchemaPropertiesLabel'
import MemoComponent from 'src/components/commons/MemoComponent'
import ModuleGraph, {RANGES} from 'src/components/commons/ModuleGraph'


/**
 * MessageBoxエリア
 */
class MessageBoxPaper extends Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    messageBox: PropTypes.object.isRequired,
    schema: PropTypes.object.isRequired,
    onEditTouchTap: PropTypes.func,
    onDeleteTouchTap: PropTypes.func,
    onDownloadTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
        module,
        messageBox,
        schema,
        onEditTouchTap,
        onDeleteTouchTap,
        onDownloadTouchTap,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'row nowrap',
        padding: 24,
      },

      graphSection: {
        display: 'flex',
        justifyContent: 'center',
        paddingLeft: 24,
      },
      graph: {
        width: '100%',
      },

      displayName: {
        paddingTop: 16,
        paddingLeft: 24,
        fontSize: 14,
        fontWeight: 'bold',
      },

      schemaSection: {
        paddingTop: 16,
      },
      schemaPropertyDisplayName: {
        fontSize: 14,
      },

      memoSection: {
        paddingTop: 16,
      },

      dataInfoSection: {
        display: 'flex',
        justifyContent: 'center',
        paddingTop: 24,
      },

      actionsSection: {
        display: 'flex',
        justifyContent: 'center',
        paddingTop: 24,
      },

    }

    console.log(module)
    return (
      <Paper>
        <div style={style.root}>
          <ComponentWithMoreIconMenu
            menuItems={[
              <MenuItem
                primaryText="このメッセージボックスを編集する"
                leftIcon={<EditIcon />}
                onTouchTap={onEditTouchTap}
              />,
              <MenuItem
                primaryText="このメッセージボックスを削除する"
                leftIcon={<DeleteIcon />}
                onTouchTap={onDeleteTouchTap}
              />,
            ]}
          >
            <div style={style.graphSection}>
              <div style={style.graph}>
                <ModuleGraph
                  module={module}
                  messageBox={messageBox}
                  range={RANGES[0]}
                  autoUpdate={0}
                />
              </div>
            </div>

            <div style={style.displayName}>
              {messageBox.displayName || '(no name)'}
            </div>

            <div style={style.schemaSection}>
              <ComponentWithSubTitle subTitle="メッセージスキーマ" icon={SchemaIcon}>
                <div style={style.schemaPropertyDisplayName}>{schema.displayName}</div>
                <SchemaPropertiesLabel schema={schema}/>
              </ComponentWithSubTitle>
            </div>

            <div style={style.memoSection}>
              <MemoComponent obj={messageBox}/>
            </div>

            <div style={style.dataInfoSection}>
              <ComponentWithSubTitle subTitle="更新情報">
                <div style={{background: '#EEE', width: '100%', height: 60}}>
                  更新情報
                </div>
              </ComponentWithSubTitle>
            </div>

            <div style={style.actionsSection}>
              <CCFlatButton
                label="データダウンロード"
                primary={true}
                icon={DownloadIcon}
                onTouchTap={onDownloadTouchTap}
              />
            </div>
          </ComponentWithMoreIconMenu>
        </div>
      </Paper>
    )
  }
}


export default MessageBoxPaper
