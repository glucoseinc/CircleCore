import React, {Component, PropTypes} from 'react'

import {GridList, GridTile} from 'material-ui/GridList'

import {AddButton} from '../../components/buttons'
import CCLink from '../../components/CCLink'
import ModulesTable from '../../components/ModulesTable'
import InputTextField from '../../containers/InputTextField'
import {urls} from '../../routes'


/**
 */
class ModulesList extends Component {
  static propTypes = {
    modules: PropTypes.object.isRequired,
    inputText: PropTypes.string.isRequired,
    onModulesTagTouchTap: PropTypes.func,
    onDeleteTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      modules,
      inputText,
      onModulesTagTouchTap,
      onModulesDeleteTouchTap,
    } = this.props

    const filteredModules = inputText === '' ? modules : modules.filter((module) => (
      module.tags.filter((tag) => tag.includes(inputText)).size > 0
    ))


    return (
      <div>
        <GridList cols={12} cellHeight="auto">
          <GridTile cols={10}>
            <InputTextField
              hintText="タグで検索"
              fullWidth={true}
            />
          </GridTile>
          <GridTile cols={2}>
            <CCLink url={urls.modulesNew}>
              <AddButton />
            </CCLink>
          </GridTile>
        </GridList>

        <ModulesTable
          modules={filteredModules}
          onTagTouchTap={onModulesTagTouchTap}
          onDeleteTouchTap={onModulesDeleteTouchTap}
        />
      </div>
    )
  }
}


export default ModulesList
