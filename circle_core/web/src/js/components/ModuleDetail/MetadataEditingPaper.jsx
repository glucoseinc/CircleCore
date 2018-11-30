import PropTypes from 'prop-types'
import React from 'react'

import Paper from 'material-ui/Paper'

import ComponentWithOkCancelButton from 'src/components/bases/ComponentWithOkCancelButton'

import MemoTextField from 'src/components/commons/MemoTextField'
import ModuleAttributesEditComponent from 'src/components/commons/ModuleAttributesEditComponent'
import TagsEditComponent from 'src/components/commons/TagsEditComponent'


/**
 * メタデータエリア(編集状態)
 */
class MetadataEditingPaper extends React.Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    tagSuggestions: PropTypes.array,
    attributeNameSuggestions: PropTypes.array,
    attributeValueSuggestions: PropTypes.array,
    onUpdate: PropTypes.func,
    onOKButtonClick: PropTypes.func,
    onCancelButtonClick: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      module,
      tagSuggestions = [],
      attributeNameSuggestions = [],
      attributeValueSuggestions = [],
      onUpdate,
      onOKButtonClick,
      onCancelButtonClick,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'row nowrap',
        padding: 24,
      },

      contents: {
        display: 'flex',
        flexFlow: 'column nowrap',
      },
      tagsSection: {
      },
      attributesSection: {
        paddingTop: 16,
      },
      memoSection: {
        paddingTop: 16,
      },
    }

    return (
      <Paper>
        <div style={style.root}>
          <ComponentWithOkCancelButton
            okButtonLabel="保存"
            okButtonDisabled={module.isReadyToCreate() ? false : true}
            onOKButtonClick={onOKButtonClick}
            onCancelButtonClick={onCancelButtonClick}
          >
            <div style={style.contents}>
              <div style={style.tagsSection}>
                <TagsEditComponent
                  module={module}
                  suggestions={tagSuggestions}
                  onUpdate={(index, tag) => onUpdate(module.updateTag(index, tag))}
                  onDeleteClick={(index) => onUpdate(module.removeTag(index))}
                  onAddClick={() => onUpdate(module.pushTag())}
                />
              </div>
              <div style={style.attributesSection}>
                <ModuleAttributesEditComponent
                  module={module}
                  nameSuggestions={attributeNameSuggestions}
                  valueSuggestions={attributeValueSuggestions}
                  onUpdate={(index, attribute) => onUpdate(module.updateModuleAttribute(index, attribute))}
                  onDeleteClick={(index) => onUpdate(module.removeModuleAttribute(index))}
                  onAddClick={() => onUpdate(module.pushModuleAttribute())}
                />
              </div>
              <div style={style.memoSection}>
                <MemoTextField
                  obj={module}
                  onChange={(e) => onUpdate(module.updateMemo(e.target.value))}
                />
              </div>
            </div>
          </ComponentWithOkCancelButton>
        </div>
      </Paper>
    )
  }
}


export default MetadataEditingPaper
