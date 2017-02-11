import actions from 'src/actions'
import ModulesNew from 'src/containers/ModulesNew'

const modulesNewRoute = {
  key: 'modulesNew',
  path: 'modules/new',
  label: 'モジュール作成',
  // icon: null,
  component: ModulesNew,
  onEnterActions: [
    actions.schema.fetchAllRequest,
    actions.modules.fetchRequest,
  ],
}

export default modulesNewRoute
