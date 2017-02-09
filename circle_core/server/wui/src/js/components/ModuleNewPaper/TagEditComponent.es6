import React, {Component, PropTypes} from 'react'

import ComponentWithIconButton from 'src/components/bases/ComponentWithIconButton'
import {DeleteIcon} from 'src/components/bases/icons'

import TagTextField from 'src/components/commons/TagTextField'


/**
 * タグ編集コンポーネント
 */
class TagEditComponent extends Component {
  static propTypes = {
    tag: PropTypes.string.isRequired,
    suggestions: PropTypes.array,
    onUpdate: PropTypes.func,
    onDeleteTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      tag,
      suggestions = [],
      onUpdate,
      onDeleteTouchTap,
    } = this.props

    const style={
      root: {
        alignItems: 'baseline',
      },
      children: {
        flexGrow: 0,
      },
    }

    return (
      <ComponentWithIconButton
        rootStyle={style.root}
        childrenStyle={style.children}
        icon={DeleteIcon}
        onIconButtonTouchTap={onDeleteTouchTap}
      >
        <TagTextField
          tag={tag}
          suggestions={suggestions}
          onChange={onUpdate}
        />
      </ComponentWithIconButton>
    )
  }
}

export default TagEditComponent
