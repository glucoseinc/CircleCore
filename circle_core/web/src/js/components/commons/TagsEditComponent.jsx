import PropTypes from 'prop-types'
import React from 'react'

import AddFlatButton from 'src/components/commons/AddFlatButton'
import TagEditComponent from 'src/components/commons/TagEditComponent'


/**
 * タグ編集コンポーネント
 */
class TagsEditComponent extends React.Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    suggestions: PropTypes.array,
    onUpdate: PropTypes.func,
    onDeleteClick: PropTypes.func,
    onAddClick: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      module,
      suggestions = [],
      onUpdate,
      onDeleteClick,
      onAddClick,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
        width: '100%',
      },

      tags: {
        marginTop: -8,
      },
      tagBlock: {
        paddingTop: 8,
      },

      actionsBlock: {
        paddingTop: 16,
      },
    }

    const optimizedSuggestions = suggestions.filter((suggestion) => !module.tags.includes(suggestion))

    return (
      <div style={style.root}>
        <div style={style.tags}>
          {module.tags.valueSeq().map((tag, index) => {
            const error = tag.length !== 0 && module.tags.filter((_tag) => _tag === tag).size > 1
            return (
              <div key={index} style={style.tagBlock}>
                <TagEditComponent
                  tag={tag}
                  suggestions={optimizedSuggestions}
                  error={error}
                  onUpdate={(newTag) => onUpdate(index, newTag)}
                  onDeleteClick={() => onDeleteClick(index)}
                />
              </div>
            )
          })}
        </div>
        <div style={style.actionsBlock}>
          <AddFlatButton
            label="タグを追加する"
            onClick={onAddClick}
          />
        </div>
      </div>
    )
  }
}

export default TagsEditComponent
