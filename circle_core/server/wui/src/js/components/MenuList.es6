import React, {Component, PropTypes} from 'react'

import Divider from 'material-ui/Divider'
import {List, ListItem} from 'material-ui/List'
import Subheader from 'material-ui/Subheader'

import {colorMenuListItemText} from '../colors'


/**
 */
class MenuSection extends Component {
  static propTypes = {
    section: PropTypes.object.isRequired,
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

    const style = {
      title: {
        lineHeight: '32px',
        fontSize: 12,
        paddingLeft: 24,
        paddingRight: 24,
      },
      item: {
        fontSize: 14,
        paddingLeft: 8,
        paddingRight: 0,
        color: colorMenuListItemText,
      },
    }

    const sectionDivider = index !== 0 ? <Divider /> : null
    const title = section.title !== null ? <Subheader style={style.title}>{section.title}</Subheader> : null

    return (
      <div>
        {sectionDivider}
        {title}
        {section.items.map((item, itemIndex) =>
          <ListItem
            key={itemIndex}
            style={style.item}
            primaryText={item.text}
            leftIcon={item.icon ? <item.icon color={colorMenuListItemText} /> : null}
            onTouchTap={onItemTouchTap ? () => onItemTouchTap(item.value) : () => null}
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
