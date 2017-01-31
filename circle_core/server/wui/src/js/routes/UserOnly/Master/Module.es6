import actions from 'src/actions'
import Module from 'src/containers/Module'

const moduleRoute = {
  key: 'module',
  path: 'modules/:moduleId',
  label: 'モジュール詳細',
  // icon: null,
  component: Module,
  onEnterActions: [
    actions.module.fetchRequest,
    actions.schemas.fetchRequest,
  ],
}

export default moduleRoute
