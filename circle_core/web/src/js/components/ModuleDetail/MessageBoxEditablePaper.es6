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
import ModuleGraphTimeRange from 'src/components/commons/ModuleGraphTimeRange'

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
    editDisabled: PropTypes.bool,
    deleteDisabled: PropTypes.bool,
    fetchingData: PropTypes.object.isRequired,
    onEditTouchTap: PropTypes.func,
    onDeleteTouchTap: PropTypes.func,
    onDownloadTouchTap: PropTypes.func,
  }

  state = {
    graphRange: RANGES[0],
    downloadStartDate: null,
    downloadEndDate: null,
  }

  /**
   * @override
   */
  render() {
    const {
      graphRange,
      downloadStartDate,
      downloadEndDate,
    } = this.state
    const {
      module,
      messageBoxIndex,
      schemas,
      editDisabled = false,
      deleteDisabled = false,
      fetchingData,
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

      graphSection: {
        marginLeft: 24,
        position: 'relative',
        background: grey100,
      },
      timeRange: {
      },
      graph: {
        paddingTop: 8,
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
        marginTop: 24,
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
        <MoreIconMenu>
          <MenuItem
            primaryText="このメッセージボックスを編集する"
            disabled={editDisabled}
            leftIcon={<EditIcon />}
            onTouchTap={onEditTouchTap}
          />
          <MenuItem
            primaryText="このメッセージボックスを削除する"
            disabled={editDisabled || deleteDisabled}
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
          <ModuleGraphTimeRange
            activeTimeRange={graphRange}
            style={style.timeRange}
            onTouchTap={(range) => this.setState({graphRange: range})}
          />
          <div style={style.graph}>
            <ModuleGraph
              module={module}
              messageBox={messageBox}
              range={graphRange}
              autoUpdate={0}
            />
          </div>
        </div>

        <ComponentWithSubTitle subTitle="メッセージスキーマ" icon={SchemaIcon} style={style.schemaSection}>
          <div style={style.schemaPropertyDisplayName}>{schema.displayName}</div>
          <SchemaPropertiesLabel schema={schema} />
        </ComponentWithSubTitle>

        <MemoComponent obj={messageBox} style={style.memoSection} />

        <ComponentWithSubTitle subTitle="更新情報" style={style.dataInfoSection}>
          <MessageBoxDataInfo
            module={module}
            messageBox={messageBox}
            fetchingData={fetchingData}
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
