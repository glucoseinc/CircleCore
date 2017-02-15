import actions from 'src/actions'
import {ModuleIcon} from 'src/components/bases/icons'
import Modules from 'src/containers/Modules'

const modulesRoute = {
  key: 'modules',
  path: 'modules',
  label: 'モジュール一覧',
  icon: ModuleIcon,
  component: Modules,
  onEnterActions: [
    actions.module.fetchAllRequest,
  ],
}

export default modulesRoute
