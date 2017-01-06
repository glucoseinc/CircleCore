import React, {Component, PropTypes} from 'react'

import Divider from 'material-ui/Divider'
import {List, ListItem} from 'material-ui/List'
import Subheader from 'material-ui/Subheader'


/**
 */
class MenuBlock extends Component {
  static propTypes = {
    block: PropTypes.object.isRequired,
    index: PropTypes.number,
    onTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {block} = this.props

    const title = block.title !== null ? <Subheader>{block.title}</Subheader> : null

    return (
      <div>
        {title}
        {block.items.map((item, itemIndex) =>
          <ListItem
            key={itemIndex}
            primaryText={item.text}
            onTouchTap={() => ::this.handleOnTouchTap(item.value)}
          />
        )}
      </div>
    )
  }

  /**
   * @param {string} value
   */
  handleOnTouchTap(value) {
    const {onTouchTap} = this.props
    if (onTouchTap !== undefined) {
      onTouchTap(value)
    }
  }
}


/**
 */
class MenuSection extends Component {
  static propTypes = {
    section: PropTypes.array.isRequired,
    index: PropTypes.number.isRequired,
    onItemTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      section,
      index,
      onItemTouchTap,
    } = this.props

    const sectionDivider = index !== 0 ? <Divider /> : null

    return (
      <div>
        {sectionDivider}
        {section.map((block, blockIndex) =>
          <MenuBlock
            key={blockIndex}
            block={block}
            index={blockIndex}
            onTouchTap={onItemTouchTap}
          />
        )}
      </div>
    )
  }
}


/**
 */
class MenuList extends Component {
  static propTypes = {
    sections: PropTypes.array.isRequired,
    onItemTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      sections,
      onItemTouchTap,
    } = this.props

    return (
      <List>
        {sections.map((section, sectionIndex) =>
          <MenuSection
            key={sectionIndex}
            section={section}
            index={sectionIndex}
            onItemTouchTap={onItemTouchTap}
          />
        )}
      </List>
    )
  }
}

export default MenuList
