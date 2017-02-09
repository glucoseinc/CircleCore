import React, {Component, PropTypes} from 'react'

import DatePicker from 'material-ui/DatePicker'
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
    messageBoxIndex: PropTypes.number.isRequired,
    schema: PropTypes.object.isRequired,
    deleteDispabled: PropTypes.bool,
    onEditTouchTap: PropTypes.func,
    onDeleteTouchTap: PropTypes.func,
    onDownloadTouchTap: PropTypes.func,
  }

  state = {
    downloadStartDate: null,
    downloadEndDate: null,
  }

  /**
   * @override
   */
  render() {
    const {
      downloadStartDate,
      downloadEndDate,
    } = this.state
    const {
      module,
      messageBoxIndex,
      schema,
      deleteDispabled = false,
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

      downloadSection: {
        display: 'flex',
        flexFlow: 'column nowrap',
        justifyContent: 'center',
        paddingTop: 24,
      },
      dateRange: {
        display: 'flex',
        flexFlow: 'row nowrap',
        justifyContent: 'center',
        alignItems: 'center',
      },
      rangeMark: {
        padding: '0 8px',
      },
      downloadButton: {
        display: 'flex',
        justifyContent: 'center',
      },
    }

    const messageBox = module.messageBoxes.get(messageBoxIndex)

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
                disabled={deleteDispabled}
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

            <div style={style.downloadSection}>
              <div style={style.dateRange}>
                <DatePicker
                  hintText="開始日"
                  container="inline"
                  onChange={(n, date) => this.setState({
                    downloadStartDate: date,
                  })}
                />
                <span style={style.rangeMark}>〜</span>
                <DatePicker
                  hintText="終了日"
                  container="inline"
                  onChange={(n, date) => this.setState({
                    downloadEndDate: date,
                  })}
                />
              </div>
              <div style={style.downloadButton}>
                <CCFlatButton
                  label="データダウンロード"
                  primary={true}
                  icon={DownloadIcon}
                  disabled={downloadStartDate === null || downloadEndDate === null ? true : false}
                  onTouchTap={() => onDownloadTouchTap(module, messageBox, downloadStartDate, downloadEndDate)}
                />
              </div>
            </div>
          </ComponentWithMoreIconMenu>
        </div>
      </Paper>
    )
  }
}


export default MessageBoxPaper
