import React, {Component, PropTypes} from 'react'

import ModulesTable from '../../components/ModulesTable'


/**
 */
class ModulesList extends Component {
  static propTypes = {
    modules: PropTypes.object.isRequired,
    onModulesTagTouchTap: PropTypes.func,
    onDeleteTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      modules,
      onModulesTagTouchTap,
      onModulesDeleteTouchTap,
    } = this.props

    return (
      <ModulesTable
        modules={modules}
        onTagTouchTap={onModulesTagTouchTap}
        onDeleteTouchTap={onModulesDeleteTouchTap}
      />
    )
  }
}


export default ModulesList
