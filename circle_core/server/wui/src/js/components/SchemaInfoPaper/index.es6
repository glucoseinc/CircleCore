import React, {Component, PropTypes} from 'react'

import Paper from 'material-ui/Paper'
import ActionDelete from 'material-ui/svg-icons/action/delete'

import DisplayNameLabel from './DisplayNameLabel'
import MemoArea from './MemoArea'
import ModuleButton from './ModuleButton'
import MoreMenu from './MoreMenu'
import MoreMenuItem from './MoreMenuItem'
import ReplicationMasterInfoChip from './ReplicationMasterInfoChip'
import SchemaPropertyLabel from './SchemaPropertyLabel'


/**
 */
class SchemaInfoPaper extends Component {
  static propTypes = {
    schema: PropTypes.object.isRequired,
    modules: PropTypes.object.isRequired,
    onTouchTap: PropTypes.func,
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
        padding: 0,
      },
      properties: {
        display: 'flex',
        flexFlow: 'row wrap',
        flexGrow: 1,
        padding: 0,
      },
      property: {
        padding: 4,
      },
      moreButton: {
        margin: '2px 0',
        padding: 4,
        height: 24,
      },

      modules: {
        display: 'flex',
        flexFlow: 'row wrap',
        padding: 0,
      },
      module: {
        padding: 4,
      },

      memo: {
        padding: 4,
        overflow: 'auto',
        wordWrap: 'break-word',
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
            <div style={style.displayName}><DisplayNameLabel schema={schema} /></div>
            <div style={style.replicationMasterInfo}>
              {replicationMaster ? <ReplicationMasterInfoChip replicationMaster={replicationMaster} /> : null}
            </div>
          </div>
          <div style={style.right}>
            <div style={style.rightTop}>
              <div style={style.properties}>
                {schema.properties.valueSeq().map((property, index) => (
                  <div key={index} style={style.property}>
                    <SchemaPropertyLabel
                      schemaProperty={property}
                    />
                  </div>
                ))}
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
            <div style={style.modules} onTouchTap={(e) => e.stopPropagation()}>
              {schema.modules.valueSeq().map((moduleId) => (
                <div key={moduleId} style={style.module}>
                  <ModuleButton
                    module={modules.get(moduleId)}
                    onTouchTap={onModuleButtonTouchTap}
                  />
                </div>
                ))}
            </div>
            <div style={style.memo}><MemoArea schema={schema} /></div>
          </div>
        </div>
      </Paper>
    )
  }
}


export default SchemaInfoPaper
