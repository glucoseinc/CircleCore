import React, {Component, PropTypes} from 'react'

import MenuItem from 'material-ui/MenuItem'
import SelectField from 'material-ui/SelectField'


/**
 */
class PropertyTypeSelectField extends Component {
  static propTypes = {
    property: PropTypes.object.isRequired,
    propertyTypes: PropTypes.object.isRequired,
    onChange: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      property,
      propertyTypes,
      onChange,
    } = this.props

    return (
      <SelectField
        floatingLabelText="属性タイプ"
        fullWidth={true}
        value={property.type}
        onChange={onChange}
      >
        {propertyTypes.valueSeq().map((propertyType) =>
          <MenuItem
            key={propertyType.name}
            value={propertyType.name}
            primaryText={propertyType.name}
          />
        )}
      </SelectField>

    )
  }
}

export default PropertyTypeSelectField
