import React, {Component, PropTypes} from 'react'

import MenuItem from 'material-ui/MenuItem'
import SelectField from 'material-ui/SelectField'


/**
 * Schemaセレクトフィールド
 */
class SchemaSelectField extends Component {
  static propTypes = {
    selectedSchemaId: PropTypes.string.isRequired,
    schemas: PropTypes.object.isRequired,
    onChange: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      selectedSchemaId,
      schemas,
      onChange,
      ...other
    } = this.props

    return (
      <SelectField
        floatingLabelText="メッセージスキーマ"
        fullWidth={true}
        value={selectedSchemaId}
        onChange={onChange}
        {...other}
      >
        {schemas.valueSeq().map((_schema) =>
          <MenuItem
            key={_schema.uuid}
            value={_schema.uuid}
            primaryText={_schema.label}
          />
        )}
      </SelectField>
    )
  }
}

export default SchemaSelectField
