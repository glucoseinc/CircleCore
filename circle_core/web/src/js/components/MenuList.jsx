import PropTypes from 'prop-types'
import React from 'react'

import Divider from 'material-ui/Divider'
import {List, ListItem} from 'material-ui/List'
import Subheader from 'material-ui/Subheader'
import {grey400, grey600} from 'material-ui/styles/colors'


/**
 */
class MenuSection extends React.Component {
  static propTypes = {
    section: PropTypes.object.isRequired,
    selectedValue: PropTypes.string,
    index: PropTypes.number.isRequired,
    onItemTouchTap: PropTypes.func,
  }


  /**
   * @override
   */
  render() {
    const {
      section,
      selectedValue,
      index,
      onItemTouchTap,
    } = this.props

    const colorMenuListItemText = grey600

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
        {section.items.map((item, itemIndex) => {
          const selected = selectedValue !== undefined && item.value === selectedValue
          const _style = {
            ...style.item,
            backgroundColor: selected ? grey400 : null,
          }
          return (
            <ListItem
              key={itemIndex}
              style={_style}
              primaryText={item.text}
              leftIcon={item.icon ? <item.icon color={colorMenuListItemText} /> : null}
              onTouchTap={onItemTouchTap ? () => onItemTouchTap(item.value) : () => null}
            />
          )
        })}
      </div>
    )
  }
}


/**
 */
class MenuList extends React.Component {
  static propTypes = {
    sections: PropTypes.array.isRequired,
    selectedValue: PropTypes.string,
    onItemTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      sections,
      selectedValue,
      onItemTouchTap,
    } = this.props

    return (
      <List>
        {sections.map((section, sectionIndex) => (
          <MenuSection
            key={sectionIndex}
            section={section}
            selectedValue={selectedValue}
            index={sectionIndex}
            onItemTouchTap={onItemTouchTap}
          />
        ))}
      </List>
    )
  }
}

export default MenuList
