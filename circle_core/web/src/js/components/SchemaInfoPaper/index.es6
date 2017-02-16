import React, {Component, PropTypes} from 'react'

import MenuItem from 'material-ui/MenuItem'
import Paper from 'material-ui/Paper'

import {DeleteIcon} from 'src/components/bases/icons'
import MoreIconMenu from 'src/components/bases/MoreIconMenu'
import IdLabel from 'src/components/commons/IdLabel'
import MemoLabel from 'src/components/commons/MemoLabel'
import SchemaPropertiesLabel from 'src/components/commons/SchemaPropertiesLabel'
import ModuleButtons from './ModuleButtons'
import ReplicationMasterInfoChip from './ReplicationMasterInfoChip'


/**
 * Schema一覧ペーパー
 */
class SchemaInfoPaper extends Component {
  static propTypes = {
    schema: PropTypes.object.isRequired,
    modules: PropTypes.object.isRequired,
    ownCcInfo: PropTypes.object.isRequired,
    onDisplayNameTouchTap: PropTypes.func,
    onModuleButtonTouchTap: PropTypes.func,
    onDeleteTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      schema,
      modules,
      ownCcInfo,
      onDisplayNameTouchTap,
      onModuleButtonTouchTap,
      onDeleteTouchTap,
    } = this.props

    const style = {
      root: {
        padding: 24,
        position: 'relative',
      },
      leftArea: {
        float: 'left',
        width: 232,
      },
      displayName: {
        fontSize: 14,
        fontWeight: 'bold',
        cursor: 'pointer',
      },
      replicationMasterInfo: {
        paddingTop: 8,
      },
      rightArea: {
        marginLeft: 240,
      },
      idSection: {
      },
      propertiesSection: {
        paddingTop: 8,
      },
      memoSection: {
        paddingTop: 8,
      },
      moduleSection: {
        paddingTop: 8,
      },
    }

    // TODO: dummy
    // const replicationMaster = {
    //   displayName: '九州大学xx研究部',
    // }
    const replicationMaster = null
    const deleteDisabled = schema.modules.size !== 0 || schema.ccUuid !== ownCcInfo.uuid

    return (
      <Paper>
        <div style={style.root}>
          <MoreIconMenu>
            <MenuItem
              primaryText="このスキーマを削除する"
              leftIcon={<DeleteIcon />}
              disabled={deleteDisabled}
              onTouchTap={() => onDeleteTouchTap(schema)}
            />
          </MoreIconMenu>

          <div style={style.leftArea}>
            <div style={style.displayName} onTouchTap={() => onDisplayNameTouchTap(schema)}>
              {schema.displayName || '(no name)'}
            </div>

            <div style={style.replicationMasterInfo}>
              {replicationMaster ? <ReplicationMasterInfoChip replicationMaster={replicationMaster} /> : null}
            </div>
          </div>

          <div style={style.rightArea}>
            <div style={style.idSection}>
              <IdLabel
                obj={schema}
              />
            </div>

            <div style={style.propertiesSection}>
              <SchemaPropertiesLabel schema={schema}/>
            </div>

            <div style={style.memoSection}>
              <MemoLabel obj={schema}/>
            </div>

            <div style={style.moduleSection}>
              <ModuleButtons
                schema={schema}
                modules={modules}
                onTouchTap={onModuleButtonTouchTap}
              />
            </div>
          </div>
        </div>
      </Paper>
    )
  }
}

export default SchemaInfoPaper
