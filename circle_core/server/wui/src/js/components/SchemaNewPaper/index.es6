import React, {Component, PropTypes} from 'react'

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
                onDeleteTouchTap={(index) => this.setState({schema: schema.removeSchemaProperty(index)})}
                onAddTouchTap={() => this.setState({schema: schema.pushSchemaProperty()})}
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
