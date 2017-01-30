import React, {Component, PropTypes} from 'react'

import {grey900, orange700} from 'material-ui/styles/colors'


/**
 * SchemaPropertyラベル
 */
class SchemaPropertyLabel extends Component {
  static propTypes = {
    schemaProperty: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      schemaProperty,
    } = this.props

    const style = {
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
      <div>
        <span style={style.name}>
          {schemaProperty.name}
        </span>
        <span style={style.type}>
          {schemaProperty.type}
        </span>
      </div>
    )
  }
}

export default SchemaPropertyLabel
