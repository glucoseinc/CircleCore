import PropTypes from 'prop-types'
import React from 'react'
import {Set} from 'immutable'

import {Tabs, Tab} from 'material-ui/Tabs'
import {blue500, grey50} from 'material-ui/styles/colors'
import {SMALL} from 'material-ui/utils/withWidth'

import SearchTextField from 'src/components/commons/SearchTextField'

import ModuleCards from './ModuleCards'
import ModuleInfoPaper from './ModuleInfoPaper'


/**
 * Module一覧タブコンポーネント
 */
class ModulesTabComponent extends React.Component {
  static propTypes = {
    modules: PropTypes.object.isRequired,
    ccInfos: PropTypes.object.isRequired,
    width: PropTypes.number.isRequired,
    onDisplayNameClick: PropTypes.func,
    onDeleteClick: PropTypes.func,
  }

  state = {
    searchText: '',
  }

  /**
   * 検索テキストを更新
   * @param {string} newText
   */
  setSearchText(newText) {
    this.setState({
      searchText: newText,
    })
  }

  /**
   * @override
   */
  render() {
    const {
      searchText,
    } = this.state
    const {
      modules,
      ccInfos,
      width,
      onDisplayNameClick,
      onDeleteClick,
    } = this.props

    const style = {
      tabItemContainer: {
        marginLeft: 32,
        width: 192,
        backgroundColor: grey50,
      },
      tabsInkBar: {
        marginLeft: 32,
        backgroundColor: blue500,
      },
      tab: {
        fontSize: 14,
        fontWeight: 'bold',
        color: blue500,
      },
      content: {
        padding: 32,
      },
    }

    const tagSuggestions = modules.reduce(
      (tagSet, module) => tagSet.union(module.tags)
      , new Set()
    ).toArray().sort()

    const filteredModules = searchText === '' ? modules : modules.filter((module) =>
      module.tags.filter((tag) => tag.includes(searchText)).size > 0
    )

    const searchTextField = (
      <SearchTextField
        hintText="タグでモジュールを絞込"
        fullWidth={true}
        inputText={searchText}
        suggestions={tagSuggestions}
        onChange={::this.setSearchText}
      />
    )

    return (
      <Tabs
        tabItemContainerStyle={style.tabItemContainer}
        inkBarStyle={style.tabsInkBar}
      >
        <Tab style={style.tab} label="カード一覧">
          {searchTextField}
          <div style={style.content}>
            <ModuleCards
              modules={filteredModules}
              cols={width == SMALL ? 1 : 2}
              onDisplayNameClick={onDisplayNameClick}
            />
          </div>
        </Tab>

        <Tab style={style.tab} label="リスト一覧">
          {searchTextField}
          <div style={style.content}>
            {filteredModules.valueSeq().map((module) => (
              <ModuleInfoPaper
                key={module.uuid}
                module={module}
                ccInfos={ccInfos}
                onDisplayNameClick={onDisplayNameClick}
                onTagButtonClick={::this.setSearchText}
                onDeleteClick={onDeleteClick}
              />
            ))}
          </div>
        </Tab>
      </Tabs>
    )
  }
}


export default ModulesTabComponent
