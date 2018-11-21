import PropTypes from 'prop-types'
import React from 'react'

import AddFlatButton from 'src/components/commons/AddFlatButton'

import PropertyEditComponent from './PropertyEditComponent'


/**
 * SchemaProperty編集コンポーネント
 */
class PropertiesEditComponent extends React.Component {
  static propTypes = {
    schema: PropTypes.object.isRequired,
    propertyTypes: PropTypes.object.isRequired,
    onUpdate: PropTypes.func,
    onDeleteClick: PropTypes.func,
    onAddClick: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      schema,
      propertyTypes,
      onUpdate,
      onDeleteClick,
      onAddClick,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
        width: '100%',
      },

      properties: {
        marginTop: -8,
      },
      propertyBlock: {
        paddingTop: 8,
      },

      actionsBlock: {
        paddingTop: 16,
      },
    }

    return (
      <div style={style.root}>
        <div style={style.properties}>
          {schema.properties.valueSeq().map((property, index) =>
            (<div key={index} style={style.propertyBlock}>
              <PropertyEditComponent
                property={property}
                propertyTypes={propertyTypes}
                deleteDisabled={schema.properties.size <= 1}
                onUpdate={(property) => onUpdate(index, property)}
                onDeleteClick={() => onDeleteClick(index)}
              />
            </div>)
          )}
        </div>
        <div style={style.actionsBlock}>
          <AddFlatButton
            label="プロパティを追加する"
            onClick={onAddClick}
          />
        </div>
      </div>
    )
  }
}

export default PropertiesEditComponent
