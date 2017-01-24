import React, {Component, PropTypes} from 'react'

import ModuleListTable from '../../components/ModuleListTable'


/**
 */
class ModuleList extends Component {
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
      <ModuleListTable
        modules={modules}
        onTagTouchTap={onModulesTagTouchTap}
        onDeleteTouchTap={onModulesDeleteTouchTap}
      />
    )
  }
}


export default ModuleList
