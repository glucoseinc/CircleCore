import actions from 'src/actions'
import {CoreIcon} from 'src/components/bases/icons'
import Cores from 'src/containers/Cores'

const coresRoute = {
  key: 'cores',
  path: 'cores',
  label: 'CircleCore一覧',
  icon: CoreIcon,
  component: Cores,
  onEnterActions: [
    actions.ccInfos.fetchRequest,
  ],
}

export default coresRoute
