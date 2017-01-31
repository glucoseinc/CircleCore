import React, {Component, PropTypes} from 'react'

import {grey900, orange700} from 'material-ui/styles/colors'

import ComponentWithIcon from 'src/components/bases/ComponentWithIcon'
import {SchemaPryoertyIcon} from 'src/components/bases/icons'


/**
 * SchemaPropertyリストラベル
 */
class SchemaPropertiesLabel extends Component {
  static propTypes = {
    schema: PropTypes.object.isRequired,
  }


  /**
   * @override
   */
  render() {
    const {
      schema,
    } = this.props

    const style = {
      properties: {
        display: 'flex',
        flexFlow: 'row wrap',
        marginLeft: -16,
        lineHeight: 1,
      },
      property: {
        paddingLeft: 16,
      },
      name: {
        fontSize: 14,
        letterSpacing: 0.7,
        color: grey900,
      },
      type: {
        fontSize: 12,
        fontWeight: 'bold',
        letterSpacing: 0.6,
        fontFamily: 'Courier New, Courier',
        color: orange700,
      },
    }

    return (
      <ComponentWithIcon icon={SchemaPryoertyIcon}>
        <div style={style.properties}>
          {schema.properties.valueSeq().map((property, index) =>
            <span key={index} style={style.property}>
              <span style={style.name}>{property.name}</span>
              <span style={style.type}>{property.type}</span>
            </span>
          )}
        </div>
      </ComponentWithIcon>
    )
  }
}

export default SchemaPropertiesLabel
