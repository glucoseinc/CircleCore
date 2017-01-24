import ActionSettingsInputComponent from 'material-ui/svg-icons/action/settings-input-component'
import actions from '../../../actions'
import Modules from '../../../containers/Modules'

const modulesRoute = {
  key: 'modules',
  path: 'modules/',
  label: 'モジュール一覧',
  icon: ActionSettingsInputComponent,
  component: Modules,
  onEnterActions: [
    actions.modules.fetchRequest,
  ],
}

export default modulesRoute
