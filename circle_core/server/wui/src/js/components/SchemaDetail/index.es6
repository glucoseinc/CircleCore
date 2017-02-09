import React, {Component, PropTypes} from 'react'

import ComponentWithTitle from 'src/components/bases/ComponentWithTitle'

import BackButton from 'src/components/commons/BackButton'
import DeleteButton from 'src/components/commons/DeleteButton'
import DisplayNamePaper from 'src/components/commons/DisplayNamePaper'

import MetadataPaper from './MetadataPaper'
import PropertiesTableComponent from './PropertiesTableComponent'


/**
 * Schema詳細コンポーネント
 */
class SchemaDetail extends Component {
  static propTypes = {
    schema: PropTypes.object.isRequired,
    onIdCopyButtonTouchTap: PropTypes.func,
    onBackTouchTap: PropTypes.func,
    onDeleteTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      schema,
      onIdCopyButtonTouchTap,
      onBackTouchTap,
      onDeleteTouchTap,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
      },

      displayNamePaper: {
      },

      propertiesArea: {
        paddingTop: 32,
      },

      metadataArea: {
        paddingTop: 32,
      },

      actionsArea: {
        paddingTop: 40,
        display: 'flex',
        flexFlow: 'row nowrap',
        justifyContent: 'center',
      },
      backButton: {
        paddingRight: 4,
      },
      deleteButton: {
        paddingLeft: 4,
      },
    }

    const deleteButtonDisabled = schema.modules.size !== 0 ? true : false

    return (
      <div style={style.root}>
        <div style={style.displayNamePaper}>
          <DisplayNamePaper
            obj={schema}
            secondayType="id"
            onCopyButtonTouchTap={onIdCopyButtonTouchTap}
          />
        </div>

        <div style={style.propertiesArea}>
          <ComponentWithTitle title="プロパティ">
            <PropertiesTableComponent schema={schema}/>
          </ComponentWithTitle>
        </div>

        <div style={style.metadataArea}>
          <ComponentWithTitle title="メタデータ">
            <MetadataPaper schema={schema} />
          </ComponentWithTitle>
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
