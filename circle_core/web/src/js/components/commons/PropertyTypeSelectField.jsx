import PropTypes from 'prop-types'
import React from 'react'

import MenuItem from 'material-ui/MenuItem'
import SelectField from 'material-ui/SelectField'


/**
 * PropertyTypeセレクトフィールド
 */
class PropertyTypeSelectField extends React.Component {
  static propTypes = {
    selectedProperty: PropTypes.object.isRequired,
    propertyTypes: PropTypes.object.isRequired,
    onChange: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      selectedProperty,
      propertyTypes,
      onChange,
    } = this.props

    return (
      <SelectField
        floatingLabelText="属性タイプ"
        fullWidth={true}
        value={selectedProperty.type}
        onChange={onChange}
      >
        {propertyTypes.valueSeq().map((propertyType) => (
          <MenuItem
            key={propertyType.name}
            value={propertyType.name}
            primaryText={propertyType.name}
          />
        ))}
      </SelectField>
    )
  }
}

export default PropertyTypeSelectField
