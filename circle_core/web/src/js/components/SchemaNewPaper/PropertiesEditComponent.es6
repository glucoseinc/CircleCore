import React, {Component, PropTypes} from 'react'

import AddFlatButton from 'src/components/commons/AddFlatButton'

import PropertyEditComponent from './PropertyEditComponent'


/**
 * SchemaProperty編集コンポーネント
 */
class PropertiesEditComponent extends Component {
  static propTypes = {
    schema: PropTypes.object.isRequired,
    propertyTypes: PropTypes.object.isRequired,
    onUpdate: PropTypes.func,
    onDeleteTouchTap: PropTypes.func,
    onAddTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      schema,
      propertyTypes,
      onUpdate,
      onDeleteTouchTap,
      onAddTouchTap,
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
            <div key={index} style={style.propertyBlock}>
              <PropertyEditComponent
                property={property}
                propertyTypes={propertyTypes}
                deleteDisabled={schema.properties.size <= 1}
                onUpdate={(property) => onUpdate(index, property)}
                onDeleteTouchTap={() => onDeleteTouchTap(index)}
              />
            </div>
          )}
        </div>
        <div style={style.actionsBlock}>
          <AddFlatButton
            label="プロパティを追加する"
            onTouchTap={onAddTouchTap}
          />
        </div>
      </div>
    )
  }
}

export default PropertiesEditComponent
