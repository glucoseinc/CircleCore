import React, {Component, PropTypes} from 'react'

import Paper from 'material-ui/Paper'
import ActionDelete from 'material-ui/svg-icons/action/delete'

import DisplayNameLabel from '../commons/DisplayNameLabel'
import IdLabel from '../commons/IdLabel'
import MemoLabel from '../commons/MemoLabel'
import MoreMenu from '../commons/MoreMenu'
import MoreMenuItem from '../commons/MoreMenuItem'
import ModuleButtons from './ModuleButtons'
import ReplicationMasterInfoChip from './ReplicationMasterInfoChip'
import SchemaPropertiesLabel from './SchemaPropertiesLabel'


/**
 * Schemaリストの1Schema
 */
class SchemaInfoPaper extends Component {
  static propTypes = {
    schema: PropTypes.object.isRequired,
    modules: PropTypes.object.isRequired,
    onTouchTap: PropTypes.func,
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
      onTouchTap,
      onIdCopyButtonTouchTap,
      onModuleButtonTouchTap,
      onDeleteTouchTap,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'row nowrap',
        padding: 8,
        cursor: 'pointer',
      },

      left: {
        display: 'flex',
        flexFlow: 'column nowrap',
        padding: 8,
        boxSizing: 'border-box',
        minWidth: 232,
        maxWidth: 232,
      },
      displayName: {
        padding: 8,
        lineHeight: 1,
      },
      replicationMasterInfo: {
        padding: 8,
      },

      right: {
        display: 'flex',
        flexFlow: 'column nowrap',
        flexGrow: 1,
        padding: 8,
        minWidth: 0,
      },
      rightTop: {
        display: 'flex',
        flexFlow: 'row nowrap',
        padding: 8,
      },
      idAndProperties: {
        display: 'flex',
        flexFlow: 'column nowrap',
        flexGrow: 1,
      },
      id: {
        padding: 0,
      },
      properties: {
        display: 'flex',
        flexFlow: 'row wrap',
        paddingTop: 8,
      },
      property: {
        padding: 4,
      },
      moreButton: {
        margin: '2px 0',
        padding: 4,
        height: 24,
      },

      memo: {
        padding: '0 8px',
      },

      modules: {
        display: 'flex',
        flexFlow: 'row wrap',
        padding: 8,
        paddingBottom: 0,
      },
      module: {
        padding: 4,
      },
    }

    // TODO: dummy
    // const replicationMaster = {
    //   displayName: '九州大学xx研究部',
    // }
    const replicationMaster = null

    return (
      <Paper>
        <div style={style.root} onTouchTap={() => onTouchTap(schema)}>
          <div style={style.left}>
            <div style={style.displayName}><DisplayNameLabel obj={schema} /></div>
            <div style={style.replicationMasterInfo}>
              {replicationMaster ? <ReplicationMasterInfoChip replicationMaster={replicationMaster} /> : null}
            </div>
          </div>

          <div style={style.right}>
            <div style={style.rightTop}>
              <div style={style.idAndProperties}>
                <div style={style.id}>
                  <IdLabel
                    obj={schema}
                    onTouchTap={onIdCopyButtonTouchTap}
                  />
                </div>
                <div style={style.properties}>
                  <SchemaPropertiesLabel
                    schema={schema}
                  />
                </div>
              </div>
              <div style={style.moreButton} onTouchTap={(e) => e.stopPropagation()}>
                <MoreMenu>
                  <MoreMenuItem
                    primaryText="このスキーマを削除する"
                    leftIcon={ActionDelete}
                    disabled={schema.modules.size === 0 ? false : true}
                    onTouchTap={() => onDeleteTouchTap(schema)}
                  />
                </MoreMenu>
              </div>
            </div>

            <div style={style.memo}><MemoLabel obj={schema}/></div>

            <div style={style.modules}>
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
