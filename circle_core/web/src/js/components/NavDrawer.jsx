import PropTypes from 'prop-types'
import React from 'react'

import AppBar from 'material-ui/AppBar'
import Drawer from 'material-ui/Drawer'

import {urls} from 'src/routes'

import CCLink from 'src/components/commons/CCLink'

import MenuList from 'src/components/MenuList'


/**
 * [mapURLToMenuItem description]
 * @param  {[type]} url [description]
 * @return {[type]}     [description]
 */
function mapURLToMenuItem(url) {
  return {
    text: url.label,
    icon: url.icon,
    value: url.fullPath,
  }
}


/**
 */
class NavDrawer extends React.Component {
  static propTypes = {
    location: PropTypes.object,
    alwaysOpen: PropTypes.bool.isRequired,
    open: PropTypes.bool.isRequired,
    onRequestChange: PropTypes.func.isRequired,
    onNavItemClick: PropTypes.func.isRequired,
  }

  /**
   * @override
   */
  render() {
    const menuSections = [
      {
        title: '構成管理',
        items: [
          mapURLToMenuItem(urls.modules),
          mapURLToMenuItem(urls.schemas),
        ],
      },
      {
        title: '同期',
        items: [
          mapURLToMenuItem(urls.replicas),
          mapURLToMenuItem(urls.replicationMasters),
        ],
      },
      {
        title: 'ユーザ管理',
        items: [
          mapURLToMenuItem(urls.users),
          mapURLToMenuItem(urls.invitations),
        ],
      },
      {
        title: null,
        items: [
          mapURLToMenuItem(urls.setting),
          mapURLToMenuItem(urls.changeProfile),
          mapURLToMenuItem(urls.logout),
        ],
      },
    ]

    const {
      location,
      alwaysOpen,
      open,
      onRequestChange,
      onNavItemClick,
    } = this.props

    const docked = alwaysOpen ? true : false

    return (
      <Drawer
        docked={docked}
        open={alwaysOpen || open}
        onRequestChange={onRequestChange}
      >
        <CCLink url={urls.root}>
          <AppBar
            iconElementLeft={<div />}
            title="CircleCore"
          />
        </CCLink>

        <MenuList
          sections={menuSections}
          selectedValue={location.pathname}
          onItemClick={onNavItemClick}
        />
      </Drawer>
    )
  }
}

export default NavDrawer
