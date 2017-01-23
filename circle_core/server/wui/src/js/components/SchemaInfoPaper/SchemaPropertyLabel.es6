import React, {Component, PropTypes} from 'react'

import {grey300, grey900} from 'material-ui/styles/colors'


/**
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
      root: {
        height: 28,
        borderRadius: 2,
        backgroundColor: grey300,
      },
      label: {
        fontSize: 14,
        color: grey900,
        padding: 7,
      },
    }
    return (
      <div style={style.root}>
        <span style={style.label}>
          {schemaProperty.name}/{schemaProperty.type}
        </span>
      </div>
    )
  }
}

export default SchemaPropertyLabel
