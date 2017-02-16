import React, {Component, PropTypes} from 'react'

import Paper from 'material-ui/Paper'

import ComponentWithOkCancelButton from 'src/components/bases/ComponentWithOkCancelButton'

import MemoTextField from 'src/components/commons/MemoTextField'
import TagsEditComponent from 'src/components/commons/TagsEditComponent'


/**
 * メタデータエリア(編集状態)
 */
class MetadataEdittingPaper extends Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    tagSuggestions: PropTypes.array,
    onUpdate: PropTypes.func,
    onOKButtonTouchTap: PropTypes.func,
    onCancelButtonTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      module,
      tagSuggestions = [],
      onUpdate,
      onOKButtonTouchTap,
      onCancelButtonTouchTap,
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
            onOKButtonTouchTap={onOKButtonTouchTap}
            onCancelButtonTouchTap={onCancelButtonTouchTap}
          >
            <div style={style.contents}>
              <div style={style.tagsSection}>
                <TagsEditComponent
                  module={module}
                  suggestions={tagSuggestions}
                  onUpdate={(index, tag) => onUpdate(module.updateTag(index, tag))}
                  onDeleteTouchTap={(index) => onUpdate(module.removeTag(index))}
                  onAddTouchTap={() => onUpdate(module.pushTag())}
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


export default MetadataEdittingPaper
