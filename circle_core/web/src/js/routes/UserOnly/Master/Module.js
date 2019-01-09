import actions from 'src/actions'
import Module from 'src/containers/Module'

const moduleRoute = {
  key: 'module',
  path: 'modules/:moduleId([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})',
  label: 'モジュール詳細',
  // icon: null,
  component: Module,
  onEnterActions: [
    actions.module.fetchRequest,
  ],
}

export default moduleRoute
