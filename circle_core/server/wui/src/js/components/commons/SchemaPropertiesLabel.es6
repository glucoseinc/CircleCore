import React, {Component, PropTypes} from 'react'

import {grey900, orange700} from 'material-ui/styles/colors'

import ComponentWithIcon from 'src/components/bases/ComponentWithIcon'
import {SchemaPryoertyIcon} from 'src/components/bases/icons'


/**
 * スキーマの型1個分
 */
export class SchemaPropertyLabel extends Component {
  static propTypes = {
    name: PropTypes.string.isRequired,
    type: PropTypes.string.isRequired,
    style: PropTypes.object,
    nameStyle: PropTypes.object,
    typeStyle: PropTypes.object,
  }

  /**
   * @override
   */
  render() {
    const styles = {
      style: {
        fontSize: 14,
        ...(this.props.style || {}),
      },
      name: {
        letterSpacing: 0.7,
        color: grey900,
        ...(this.props.nameStyle || {}),
      },
      type: {
        fontSize: '85%',
        fontWeight: 'bold',
        letterSpacing: 0.6,
        fontFamily: 'Courier New, Courier',
        color: orange700,
        marginRight: 4,
        ...(this.props.typeStyle || {}),
      },
    }
    return (
      <span style={styles.style}>
        <span style={styles.type}>{this.props.type}</span>
        <span style={styles.name}>{this.props.name}</span>
      </span>
    )
  }
}


/**
 * SchemaPropertyリストラベル
 */
export default class SchemaPropertiesLabel extends Component {
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
    }

    return (
      <ComponentWithIcon icon={SchemaPryoertyIcon}>
        <div style={style.properties}>
          {schema.properties.valueSeq().map((property, index) =>
            <SchemaPropertyLabel key={index} style={style.property} name={property.name} type={property.type} />
          )}
        </div>
      </ComponentWithIcon>
    )
  }
}
