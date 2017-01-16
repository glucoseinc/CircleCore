import React, {Component, PropTypes} from 'react'

import AppBar from 'material-ui/AppBar'
import Drawer from 'material-ui/Drawer'

import CCLink from '../components/CCLink'
import MenuList from '../components/MenuList'
import {urls} from '../routes'


/**
 * [mapURLToMenuItem description]
 * @param  {[type]} url [description]
 * @return {[type]}     [description]
 */
function mapURLToMenuItem(url) {
  return {
    text: url.label,
    value: url.fullPath,
  }
}


/**
 */
class NavDrawer extends Component {
  static propTypes = {
    alwaysOpen: PropTypes.bool.isRequired,
    open: PropTypes.bool.isRequired,
    onRequestChange: PropTypes.func.isRequired,
    onNavItemTouchTap: PropTypes.func.isRequired,
  }

  /**
   * @override
   */
  render() {
    const menuSections = [
      [
        {
          title: '構成管理',
          items: [
            mapURLToMenuItem(urls.modules),
            mapURLToMenuItem(urls.schemas),
          ],
        },
        // {
        //   title: '同期',
        //   items: [
        //     mapURLToMenuItem(urls.replicas),
        //   ],
        // },
        // {
        //   title: 'ダウンロード',
        //   items: [
        //     mapURLToMenuItem(urls.dumps),
        //   ],
        // },
        {
          title: 'ユーザ管理',
          items: [
            mapURLToMenuItem(urls.users),
            mapURLToMenuItem(urls.invitations),
          ],
        },
      ],
      [
        {
          title: null,
          items: [
            mapURLToMenuItem(urls.changeProfile),
            mapURLToMenuItem(urls.logout),
          ],
        },
      ],
    ]

    const {
      alwaysOpen,
      open,
      onRequestChange,
      onNavItemTouchTap,
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
            iconElementLeft={<div/>}
            title="CircleCore"
          />
        </CCLink>

        <MenuList
          sections={menuSections}
          onItemTouchTap={onNavItemTouchTap}
        />
      </Drawer>
    )
  }
}

export default NavDrawer
