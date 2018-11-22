import PropTypes from 'prop-types'
import React from 'react'

import Paper from 'material-ui/Paper'

import Schema from 'src/models/Schema'

import ComponentWithHeader from 'src/components/bases/ComponentWithHeader'

import CreateButton from 'src/components/commons/CreateButton'
import DisplayNameTextField from 'src/components/commons/DisplayNameTextField'
import MemoTextField from 'src/components/commons/MemoTextField'

import PropertiesEditComponent from './PropertiesEditComponent'


/**
 * Schema作成
 */
class SchemaNewPaper extends React.Component {
  static propTypes = {
    templateSchema: PropTypes.object,
    propertyTypes: PropTypes.object.isRequired,
    onCreateClick: PropTypes.func,
  }

  /**
   * @constructor
   */
  constructor(...args) {
    super(...args)

    this.state = {
      schema: this.props.templateSchema || new Schema().pushSchemaProperty(),
    }
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
      onCreateClick,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
        padding: 24,
      },

      displayNameArea: {
      },

      propertiesArea: {
        paddingTop: 32,
      },

      metadataArea: {
        paddingTop: 32,
      },

      actionsArea: {
        display: 'flex',
        flexFlow: 'row nowrap',
        justifyContent: 'space-around',
        paddingTop: 40,
      },
    }

    return (
      <Paper>
        <div style={style.root}>
          <div style={style.displayNameArea}>
            <DisplayNameTextField
              obj={schema}
              floatingLabelText="メッセージスキーマ名"
              onChange={(e) => this.setState({schema: schema.updateDisplayName(e.target.value)})}
            />
          </div>

          <div style={style.propertiesArea}>
            <ComponentWithHeader headerLabel="プロパティ">
              <PropertiesEditComponent
                schema={schema}
                propertyTypes={propertyTypes}
                onUpdate={(index, property) => this.setState({schema: schema.updateSchemaProperty(index, property)})}
                onDeleteClick={(index) => this.setState({schema: schema.removeSchemaProperty(index)})}
                onAddClick={() => this.setState({schema: schema.pushSchemaProperty()})}
              />
            </ComponentWithHeader>
          </div>

          <div style={style.metadataArea}>
            <ComponentWithHeader headerLabel="メタデータ">
              <div style={style.memoSection}>
                <MemoTextField
                  obj={schema}
                  onChange={(e) => this.setState({schema: schema.updateMemo(e.target.value)})}
                />
              </div>
            </ComponentWithHeader>
          </div>

          <div style={style.actionsArea}>
            <CreateButton
              disabled={schema.isReadyToCreate() ? false : true}
              onClick={() => onCreateClick(schema)}
            />
          </div>
        </div>
      </Paper>
    )
  }
}


export default SchemaNewPaper
