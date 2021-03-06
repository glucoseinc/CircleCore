import PropTypes from 'prop-types'
import React from 'react'

import Paper from 'material-ui/Paper'

import Module from 'src/models/Module'

import ComponentWithHeader from 'src/components/bases/ComponentWithHeader'

import CreateButton from 'src/components/commons/CreateButton'
import DisplayNameTextField from 'src/components/commons/DisplayNameTextField'
import MemoTextField from 'src/components/commons/MemoTextField'
import MessageBoxesEditComponent from 'src/components/commons/MessageBoxesEditComponent'
import ModuleAttributesEditComponent from 'src/components/commons/ModuleAttributesEditComponent'
import TagsEditComponent from 'src/components/commons/TagsEditComponent'


/**
 * Module作成
 */
class ModuleNewPaper extends React.Component {
  static propTypes = {
    schemas: PropTypes.object.isRequired,
    tagSuggestions: PropTypes.array,
    attributeNameSuggestions: PropTypes.array,
    attributeValueSuggestions: PropTypes.array,
    onCreateClick: PropTypes.func,
  }

  state = {
    module: new Module().pushMessageBox(),
  }

  /**
   * @override
   */
  render() {
    const {
      module,
    } = this.state
    const {
      schemas,
      tagSuggestions = [],
      attributeNameSuggestions = [],
      attributeValueSuggestions = [],
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

      metadataArea: {
        paddingTop: 32,
      },
      tagsSection: {
      },
      attributesSection: {
        paddingTop: 16,
      },
      memoSection: {
        paddingTop: 16,
      },

      messageBoxesArea: {
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
              obj={module}
              floatingLabelText="モジュール名"
              onChange={(e) => this.setState({module: module.updateDisplayName(e.target.value)})}
            />
          </div>

          <div style={style.metadataArea}>
            <ComponentWithHeader headerLabel="メタデータ">
              <div style={style.tagsSection}>
                <TagsEditComponent
                  module={module}
                  suggestions={tagSuggestions}
                  onUpdate={(index, tag) => this.setState({module: module.updateTag(index, tag)})}
                  onDeleteClick={(index) => this.setState({module: module.removeTag(index)})}
                  onAddClick={() => this.setState({module: module.pushTag()})}
                />
              </div>
              <div style={style.attributesSection}>
                <ModuleAttributesEditComponent
                  module={module}
                  nameSuggestions={attributeNameSuggestions}
                  valueSuggestions={attributeValueSuggestions}
                  onUpdate={(index, attribute) => this.setState(
                    {module: module.updateModuleAttribute(index, attribute)}
                  )}
                  onDeleteClick={(index) => this.setState({module: module.removeModuleAttribute(index)})}
                  onAddClick={() => this.setState({module: module.pushModuleAttribute()})}
                />
              </div>
              <div style={style.memoSection}>
                <MemoTextField
                  obj={module}
                  onChange={(e) => this.setState({module: module.updateMemo(e.target.value)})}
                />
              </div>
            </ComponentWithHeader>
          </div>

          <div style={style.messageBoxesArea}>
            <ComponentWithHeader headerLabel="メッセージボックス">
              <MessageBoxesEditComponent
                module={module}
                schemas={schemas}
                onUpdate={(index, messageBox) => this.setState({module: module.updateMessageBox(index, messageBox)})}
                onDeleteClick={(index) => this.setState({module: module.removeMessageBox(index)})}
                onAddClick={() => this.setState({module: module.pushMessageBox()})}
              />
            </ComponentWithHeader>
          </div>

          <div style={style.actionsArea}>
            <CreateButton
              disabled={module.isReadyToCreate() ? false : true}
              onClick={() => onCreateClick(module)}
            />
          </div>
        </div>
      </Paper>
    )
  }
}


export default ModuleNewPaper
