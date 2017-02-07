import React, {Component, PropTypes} from 'react'

import MenuItem from 'material-ui/MenuItem'
import Paper from 'material-ui/Paper'

import ComponentWithMoreIconMenu from 'src/components/bases/ComponentWithMoreIconMenu'
import {DeleteIcon} from 'src/components/bases/icons'

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
    onDisplayNameTouchTap: PropTypes.func,
    onIdCopyButtonTouchTap: PropTypes.func,
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
      onDisplayNameTouchTap,
      onIdCopyButtonTouchTap,
      onModuleButtonTouchTap,
      onDeleteTouchTap,
    } = this.props

    const style = {
      root: {
        padding: 24,
      },

      contents: {
        display: 'flex',
        flexFlow: 'row nowrap',
      },

      leftArea: {
        display: 'flex',
        flexFlow: 'column nowrap',
        minWidth: 232,
        maxWidth: 232,
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
        display: 'flex',
        flexFlow: 'column nowrap',
        flexGrow: 1,
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

    return (
      <Paper>
        <div style={style.root}>
          <ComponentWithMoreIconMenu
            menuItems={[
              <MenuItem
                primaryText="このスキーマを削除する"
                leftIcon={<DeleteIcon />}
                disabled={schema.modules.size === 0 ? false : true}
                onTouchTap={() => onDeleteTouchTap(schema)}
              />,
            ]}
          >
            <div style={style.contents}>
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
                    onTouchTap={onIdCopyButtonTouchTap}
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
          </ComponentWithMoreIconMenu>
        </div>
      </Paper>
    )
  }
}

export default SchemaInfoPaper
