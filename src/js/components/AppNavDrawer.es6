import React, {Component, PropTypes} from 'react'
import Drawer from 'material-ui/Drawer'
import {List, ListItem, makeSelectable} from 'material-ui/List'
import Divider from 'material-ui/Divider'
import Subheader from 'material-ui/Subheader'
import {spacing, typography, zIndex} from 'material-ui/styles'
import {cyan500} from 'material-ui/styles/colors'

const SelectableList = makeSelectable(List)

const styles = {
  logo: {
    cursor: 'pointer',
    fontSize: 24,
    color: typography.textFullWhite,
    lineHeight: `${spacing.desktopKeylineIncrement}px`,
    fontWeight: typography.fontWeightLight,
    backgroundColor: cyan500,
    paddingLeft: spacing.desktopGutter,
    marginBottom: 8,
  },
  version: {
    paddingLeft: spacing.desktopGutterLess,
    fontSize: 16,
  },
}

/**
 * サイト左側のナビゲーションメニュー
 */
class AppNavDrawer extends Component {
  static propTypes = {
    docked: PropTypes.bool.isRequired,
    location: PropTypes.object.isRequired,
    onChangeList: PropTypes.func.isRequired,
    onRequestChangeNavDrawer: PropTypes.func.isRequired,
    open: PropTypes.bool.isRequired,
    style: PropTypes.object,
  }

  static contextTypes = {
    muiTheme: PropTypes.object.isRequired,
    router: PropTypes.object.isRequired,
  }

  state = {
    muiVersions: [],
  }

  /**
   * @override
   */
  componentDidMount() {
    const self = this
    const url = '/versions.json'
    const request = new XMLHttpRequest()

    request.onreadystatechange = function() {
      if (request.readyState === 4 && request.status === 200) {
        self.setState({
          muiVersions: JSON.parse(request.responseText),
          version: JSON.parse(request.responseText)[0],
        })
      }
    }

    request.open('GET', url, true)
    request.send()
  }

  /**
   * @override
   */
  render() {
    const {
      location,
      docked,
      onRequestChangeNavDrawer,
      onChangeList,
      open,
      style,
    } = this.props

    return (
      <Drawer
        style={style}
        docked={docked}
        open={open}
        onRequestChange={onRequestChangeNavDrawer}
        containerStyle={{zIndex: zIndex.drawer - 100}}
      >
        <div style={styles.logo} onTouchTap={::this.handleTouchTapHeader}>
          CircleCore
        </div>

        <SelectableList
          value={location.pathname}
          onChange={onChangeList}
        >
          <Subheader>構成管理</Subheader>
          <ListItem primaryText="モジュール一覧" value="/modules/" />
          <ListItem primaryText="メッセージスキーマ一覧" value="/schemas/" />
        </SelectableList>

        <SelectableList
          value={location.pathname}
          onChange={onChangeList}
        >
          <Subheader>同期</Subheader>
          <ListItem primaryText="共有リンク一覧" value="/replicas/" />
        </SelectableList>

        <SelectableList
          value={location.pathname}
          onChange={onChangeList}
        >
          <Subheader>ダウンロード</Subheader>
          <ListItem primaryText="メッセージダウンロード" value="/dumps/" />
        </SelectableList>

        <SelectableList
          value={location.pathname}
          onChange={onChangeList}
        >
          <Subheader>ユーザ管理</Subheader>
          <ListItem primaryText="ユーザ一覧" value="/users/" />
        </SelectableList>


        <Divider />
        <SelectableList
          value={location.pathname}
          onChange={onChangeList}
        >
          <ListItem primaryText="プロフィール変更" value="/settings/me" />
          <ListItem primaryText="ログアウト" value="/logout" />
        </SelectableList>
      </Drawer>
    )
  }

  // event handlers
  /**
   * Menuのヘッダがタップされたら呼ばれる。
   * Homeに飛ぶ
   */
  handleTouchTapHeader() {
    this.context.router.push('/')
    this.props.onRequestChangeNavDrawer(false)
  }
}

export default AppNavDrawer
