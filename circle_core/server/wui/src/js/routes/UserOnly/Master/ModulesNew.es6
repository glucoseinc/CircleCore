import actions from '../../../actions'
import ModulesNew from '../../../containers/ModulesNew'

const modulesNewRoute = {
  key: 'modulesNew',
  path: 'modules/new',
  label: 'モジュール作成',
  // icon: null,
  component: ModulesNew,
  onEnterActions: [
    actions.module.createInit,
    actions.schemas.fetchRequest,
  ],
}

export default modulesNewRoute
