import PropTypes from 'prop-types'
import React from 'react'

import ComponentWithIconButton from 'src/components/bases/ComponentWithIconButton'
import {DeleteIcon} from 'src/components/bases/icons'

import PropertyNameTextField from 'src/components/commons/PropertyNameTextField'
import PropertyTypeSelectField from 'src/components/commons/PropertyTypeSelectField'


/**
 * SchemaProperty編集コンポーネント
 */
class PropertyEditComponent extends React.Component {
  static propTypes = {
    property: PropTypes.object.isRequired,
    propertyTypes: PropTypes.object.isRequired,
    deleteDisabled: PropTypes.bool,
    onUpdate: PropTypes.func,
    onDeleteTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      property,
      propertyTypes,
      deleteDisabled = false,
      onUpdate,
      onDeleteTouchTap,
    } = this.props

    const style = {
      root: {
        alignItems: 'baseline',
      },
      property: {
        display: 'flex',
        flexFlow: 'row nowrap',
      },
    }

    return (
      <ComponentWithIconButton
        rootStyle={style.root}
        icon={DeleteIcon}
        iconButtonDisabled={deleteDisabled}
        onIconButtonTouchTap={onDeleteTouchTap}
      >
        <div style={style.property}>
          <PropertyNameTextField
            property={property}
            onChange={(e) => onUpdate(property.updateName(e.target.value))}
          />
          <PropertyTypeSelectField
            selectedProperty={property}
            propertyTypes={propertyTypes}
            onChange={(e, i, v) => onUpdate(property.updateType(v))}
          />
        </div>
      </ComponentWithIconButton>
    )
  }
}

export default PropertyEditComponent
