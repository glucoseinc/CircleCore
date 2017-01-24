import React, {Component, PropTypes} from 'react'

import {grey900} from 'material-ui/styles/colors'

import DisplayNamePaper from './DosplayNamePaper'
import PropertiesTableComponent from './PropertiesTableComponent'
import MetadataPaper from './MetadataPaper'
import BackButton from './BackButton'
import DeleteButton from './DeleteButton'

/**
 * メッセージスキーマ詳細コンポーネント
 */
class SchemaDetail extends Component {
  static propTypes = {
    schema: PropTypes.object.isRequired,
    onBackTouchTap: PropTypes.func,
    onDeleteTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      schema,
      onBackTouchTap,
      onDeleteTouchTap,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
        padding: 0,
      },

      areaLabel: {
        padding: '0 24px',
        fontSize: 16,
        fontWeight: 'bold',
        lineHeight: 1,
        color: grey900,
      },

      displayNamePaper: {
        padding: 0,
        paddingBottom: 16,
      },

      propertiesArea: {
        padding: '16px 0',
      },
      propertiesTableComponent: {
        padding: 0,
      },

      metadataArea: {
        padding: '16px 0',
      },
      metadataPaper: {
        padding: '16px 0',
      },

      actionsArea: {
        padding: 4,
        display: 'flex',
        flexFlow: 'row nowrap',
        justifyContent: 'center',
      },
      backButton: {
        padding: 4,
      },
      deleteButton: {
        padding: 4,
      },
    }

    const deleteButtonDisabled = schema.modules.size !== 0 ? true : false
    return (
      <div style={style.root}>
        <div style={style.displayNamePaper}>
          <DisplayNamePaper schema={schema} />
        </div>
        <div style={style.propertiesArea}>
          <div style={style.areaLabel}>プロパティ</div>
          <div style={style.propertiesTableComponent}>
            <PropertiesTableComponent schema={schema}/>
          </div>
        </div>
        <div style={style.metadataArea}>
          <div style={style.areaLabel}>メタデータ</div>
          <div style={style.metadataPaper}>
            <MetadataPaper schema={schema} />
          </div>
        </div>
        <div style={style.actionsArea}>
          <div style={style.backButton}>
            <BackButton onTouchTap={onBackTouchTap}/>
          </div>
          <div style={style.deleteButton}>
            <DeleteButton
              disabled={deleteButtonDisabled}
              onTouchTap={onDeleteTouchTap}
            />
          </div>
        </div>
      </div>
    )
  }
}


export default SchemaDetail
