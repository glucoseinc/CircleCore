import React, {Component, PropTypes} from 'react'

import Paper from 'material-ui/Paper'
import {grey600} from 'material-ui/styles/colors'

import Schema from '../../models/Schema'
import CreateButton from './CreateButton'
import DisplayNameTextField from './DisplayNameTextField'
import MemoTextField from './MemoTextField'
import PropertyAddButton from './PropertyAddButton'
import PropertyDeleteIconButton from './PropertyDeleteIconButton'
import PropertyNameTextField from './PropertyNameTextField'
import PropertyTypeSelectField from './PropertyTypeSelectField'


/**
 */
class SchemaNewPaper extends Component {
  static propTypes = {
    propertyTypes: PropTypes.object.isRequired,
    onCreateTouchTap: PropTypes.func,
  }

  state = {
    schema: new Schema().pushSchemaProperty(),
  }

  /**
   * @override
   */
  render() {
    const {
      schema,
    } = this.state
    const {
      propertyTypes,
      onCreateTouchTap,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
        padding: 8,
      },
      areaLabel: {
        padding: 8,
        color: grey600,
      },

      displayName: {
        padding: 16,
      },

      propertiesArea: {
        display: 'flex',
        flexFlow: 'column nowrap',
        padding: 8,
      },
      properties: {
        display: 'flex',
        flexFlow: 'column nowrap',
        padding: 0,
      },
      propertyBlock: {
        display: 'flex',
        flexFlow: 'row nowrap',
        alignItems: 'center',
        padding: 0,
      },
      propertyName: {
        padding: '0px 8px',
        flexGrow: 1,
      },
      propertyType: {
        padding: '0px 8px',
        flexGrow: 1,
      },
      propertyDeleteIcon: {
        padding: '0px 8px',
      },

      propertyActionsBlock: {
        padding: 8,
      },

      metadataArea: {
        display: 'flex',
        flexFlow: 'column nowrap',
        padding: 8,
      },
      memo: {
        padding: 8,
      },

      actionsArea: {
        margin: 'auto',
        padding: 16,
      },
    }

    return (
      <Paper>
        <div style={style.root}>
          <div style={style.displayName}>
            <DisplayNameTextField
              schema={schema}
              onChange={(e) => this.setState({schema: schema.updateDisplayName(e.target.value)})}
            />
          </div>
          <div style={style.propertiesArea}>
            <div style={style.areaLabel}>
              <span>プロパティ</span>
            </div>
            <div style={style.properties}>
              {schema.properties.valueSeq().map((property, index) =>
                <div key={index} style={style.propertyBlock}>
                  <div style={style.propertyName}>
                    <PropertyNameTextField
                      property={property}
                      onChange={
                        (e) => this.setState({schema: schema.updateSchemaPropertyName(index, e.target.value)})
                      }
                    />
                  </div>
                  <div style={style.propertyType}>
                    <PropertyTypeSelectField
                      property={property}
                      propertyTypes={propertyTypes}
                      onChange={(e, i, v) => this.setState({schema: schema.updateSchemaPropertyType(index, v)})}
                    />
                  </div>
                  <div style={style.propertyDeleteIcon}>
                    <PropertyDeleteIconButton
                      onTouchTap={() => this.setState({schema: schema.removeSchemaProperty(index)})}
                    />
                  </div>
                </div>
              )}
            </div>
            <div style={style.propertyActionsBlock}>
              <PropertyAddButton
                onTouchTap={() => this.setState({schema: schema.pushSchemaProperty()})}
              />
            </div>
          </div>
          <div style={style.metadataArea}>
            <div style={style.areaLabel}>
              <span>メタデータ</span>
            </div>
            <div style={style.memo}>
              <MemoTextField
                schema={schema}
                onChange={(e) => this.setState({schema: schema.updateMemo(e.target.value)})}
              />
            </div>
          </div>
          <div style={style.actionsArea}>
            <CreateButton
              disabled={schema.isReadytoCreate() ? false : true}
              onTouchTap={() => onCreateTouchTap(schema)}
            />
          </div>
        </div>
      </Paper>
    )
  }
}


export default SchemaNewPaper