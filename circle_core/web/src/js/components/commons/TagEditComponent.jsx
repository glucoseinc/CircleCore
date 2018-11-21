import PropTypes from 'prop-types'
import React from 'react'

import ComponentWithIconButton from 'src/components/bases/ComponentWithIconButton'
import {DeleteIcon} from 'src/components/bases/icons'

import TagTextField from 'src/components/commons/TagTextField'


/**
 * タグ編集コンポーネント
 */
class TagEditComponent extends React.Component {
  static propTypes = {
    tag: PropTypes.string.isRequired,
    suggestions: PropTypes.array,
    error: PropTypes.bool,
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
      error = false,
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
          error={error}
          onChange={onUpdate}
        />
      </ComponentWithIconButton>
    )
  }
}

export default TagEditComponent
