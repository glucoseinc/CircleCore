import React, {Component, PropTypes} from 'react'

import {grey500} from 'material-ui/styles/colors'
import EditorFormatListBulleted from 'material-ui/svg-icons/editor/format-list-bulleted'

import SchemaPropertyLabel from './SchemaPropertyLabel'


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
      root: {
        display: 'flex',
        flexFlow: 'row nowrap',
        lineHeight: 1,
      },
      icon: {
        width: 16,
        height: 16,
      },
      properties: {
        display: 'flex',
        flexFlow: 'row wrap',
        flexGrow: 1,
      },
      property: {
        padding: '0 8px',
      },
    }

    return (
      <div style={style.root}>
        <EditorFormatListBulleted style={style.icon} color={grey500}/>
        <div style={style.properties}>
          {schema.properties.valueSeq().map((property, index) =>
            <div key={index} style={style.property}>
              <SchemaPropertyLabel schemaProperty={property} />
            </div>
          )}
        </div>
      </div>
    )
  }
}

export default SchemaPropertiesLabel
