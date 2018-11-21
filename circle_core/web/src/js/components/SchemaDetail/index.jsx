import PropTypes from 'prop-types'
import React from 'react'

import ComponentWithTitle from 'src/components/bases/ComponentWithTitle'

import BackButton from 'src/components/commons/BackButton'
import DeleteButton from 'src/components/commons/DeleteButton'
import DisplayNamePaper from 'src/components/commons/DisplayNamePaper'
import MetadataPaper from 'src/components/commons/MetadataPaper'
import PropertiesTableComponent from './PropertiesTableComponent'


/**
 * Schema詳細コンポーネント
 */
class SchemaDetail extends React.Component {
  static propTypes = {
    schema: PropTypes.object.isRequired,
    ownCcInfo: PropTypes.object.isRequired,
    onBackTouchTap: PropTypes.func,
    onDeleteTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      schema,
      ownCcInfo,
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

    const deleteButtonDisabled = schema.modules.size !== 0 ? true : false || schema.ccUuid !== ownCcInfo.uuid

    return (
      <div style={style.root}>
        <div style={style.displayNamePaper}>
          <DisplayNamePaper
            obj={schema}
            secondaryType={null}
          />
        </div>

        <div style={style.propertiesArea}>
          <ComponentWithTitle title="プロパティ">
            <PropertiesTableComponent schema={schema} />
          </ComponentWithTitle>
        </div>

        <div style={style.metadataArea}>
          <ComponentWithTitle title="メタデータ">
            <MetadataPaper obj={schema} />
          </ComponentWithTitle>
        </div>

        <div style={style.actionsArea}>
          <div style={style.backButton}>
            <BackButton onTouchTap={onBackTouchTap} />
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
