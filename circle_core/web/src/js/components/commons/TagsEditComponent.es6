import React, {Component, PropTypes} from 'react'

import AddFlatButton from 'src/components/commons/AddFlatButton'
import TagEditComponent from 'src/components/commons/TagEditComponent'


/**
 * タグ編集コンポーネント
 */
class TagsEditComponent extends Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    suggestions: PropTypes.array,
    onUpdate: PropTypes.func,
    onDeleteTouchTap: PropTypes.func,
    onAddTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      module,
      suggestions = [],
      onUpdate,
      onDeleteTouchTap,
      onAddTouchTap,
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

    return (
      <div style={style.root}>
        <div style={style.tags}>
          {module.tags.valueSeq().map((tag, index) => {
            const error = tag.length !== 0 && module.tags.filter((_tag) => _tag === tag).size > 1
            return (
              <div key={index} style={style.tagBlock}>
                <TagEditComponent
                  tag={tag}
                  suggestions={suggestions}
                  error={error}
                  onUpdate={(newTag) => onUpdate(index, newTag)}
                  onDeleteTouchTap={() => onDeleteTouchTap(index)}
                />
              </div>
            )
          })}
        </div>
        <div style={style.actionsBlock}>
          <AddFlatButton
            label="タグを追加する"
            onTouchTap={onAddTouchTap}
          />
        </div>
      </div>
    )
  }
}

export default TagsEditComponent
