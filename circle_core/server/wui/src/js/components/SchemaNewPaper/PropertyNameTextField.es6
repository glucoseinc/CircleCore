import React, {Component, PropTypes} from 'react'

import TextField from 'material-ui/TextField'


/**
 */
class PropertyNameTextField extends Component {
  static propTypes = {
    property: PropTypes.object.isRequired,
    onChange: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      property,
      onChange,
    } = this.props

    return (
      <TextField
        floatingLabelText="属性名"
        fullWidth={true}
        value={property.name}
        onChange={onChange}
      />
    )
  }
}

export default PropertyNameTextField
