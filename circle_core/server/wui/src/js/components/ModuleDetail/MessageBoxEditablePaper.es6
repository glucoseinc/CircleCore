import React, {Component, PropTypes} from 'react'

import {grey100} from 'material-ui/styles/colors'
import DatePicker from 'material-ui/DatePicker'
import MenuItem from 'material-ui/MenuItem'
import Paper from 'material-ui/Paper'

import CCFlatButton from 'src/components/bases/CCFlatButton'
import MoreIconMenu from 'src/components/bases/MoreIconMenu'
import ComponentWithSubTitle from 'src/components/bases/ComponentWithSubTitle'
import {DeleteIcon, DownloadIcon, EditIcon, SchemaIcon} from 'src/components/bases/icons'

import IdLabel from 'src/components/commons/IdLabel'
import SchemaPropertiesLabel from 'src/components/commons/SchemaPropertiesLabel'
import MemoComponent from 'src/components/commons/MemoComponent'
import ModuleGraph, {RANGES} from 'src/components/commons/ModuleGraph'
import MessageBoxDataInfo from './MessageBoxDataInfo'


/**
 * MessageBoxエリア(編集可能)
 */
class MessageBoxEditablePaper extends Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    messageBoxIndex: PropTypes.number.isRequired,
    schemas: PropTypes.object.isRequired,
    style: PropTypes.object,
    deleteDispabled: PropTypes.bool,
    onEditTouchTap: PropTypes.func,
    onDeleteTouchTap: PropTypes.func,
    onDownloadTouchTap: PropTypes.func,
  }

  state = {
    downloadStartDate: null,
    downloadEndDate: null,
    messageBoxDataInfoWidth: 0,
    style: {},
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
      schemas,
      deleteDispabled = false,
      onEditTouchTap,
      onDeleteTouchTap,
      onDownloadTouchTap,
    } = this.props

    const style = {
      root: {
        padding: 24,
        position: 'relative',
        ...this.props.style,
      },

      moreIconMenu: {
        position: 'absolute',
        right: 16,
        top: 16,
      },

      graphSection: {
        marginLeft: 24,
        position: 'relative',
        background: grey100,
      },
      graph: {
        width: '100%',
      },

      displayNameSection: {
        paddingLeft: 24,
        marginBottom: 16,
      },
      displayName: {
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
    require('assert')(messageBox !== undefined)
    const schema = schemas.get(messageBox.schema)
    require('assert')(schema !== undefined)

    return (
      <Paper className="messageBoxDetail" style={style.root}>
        <MoreIconMenu style={style.moreIconMenu}>
          <MenuItem
            primaryText="このメッセージボックスを編集する"
            leftIcon={<EditIcon />}
            onTouchTap={onEditTouchTap}
          />
          <MenuItem
            primaryText="このメッセージボックスを削除する"
            disabled={deleteDispabled}
            leftIcon={<DeleteIcon />}
            onTouchTap={onDeleteTouchTap}
          />
        </MoreIconMenu>

        <div style={style.displayNameSection}>
          <div style={style.displayName}>
            {messageBox.displayName || '(no name)'}
          </div>
          <IdLabel
            obj={messageBox}
          />
        </div>

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

        <div style={style.schemaSection}>
          <ComponentWithSubTitle subTitle="メッセージスキーマ" icon={SchemaIcon}>
            <div style={style.schemaPropertyDisplayName}>{schema.displayName}</div>
            <SchemaPropertiesLabel schema={schema}/>
          </ComponentWithSubTitle>
        </div>

        <div style={style.memoSection}>
          <MemoComponent obj={messageBox}/>
        </div>

        <ComponentWithSubTitle subTitle="更新情報" style={style.dataInfoSection}>
          <MessageBoxDataInfo
            module={module}
            messageBox={messageBox}
          />
        </ComponentWithSubTitle>

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
      </Paper>
    )
  }
}


export default MessageBoxEditablePaper
