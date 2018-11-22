import PropTypes from 'prop-types'
import React from 'react'

import ComponentWithIcon from 'src/components/bases/ComponentWithIcon'
import {TagIcon} from 'src/components/bases/icons'

import TagButton from './TagButton'


/**
 * Tagボタンリスト
 */
class TagButtons extends React.Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    onClick: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      module,
      onClick,
    } = this.props

    const style = {
      tags: {
        display: 'flex',
        flexFlow: 'row wrap',
        marginTop: -4,
        marginLeft: -16,
        lineHeight: 1,
      },
      tag: {
        paddingLeft: 16,
      },
    }

    return (
      <ComponentWithIcon icon={TagIcon}>
        <div style={style.tags}>
          {module.tags.valueSeq().map((tag, index) =>
            (<div key={index} style={style.tag}>
              <TagButton
                tag={tag}
                onClick={(onClick)}
              />
            </div>)
          )}
        </div>
      </ComponentWithIcon>
    )
  }
}

export default TagButtons
