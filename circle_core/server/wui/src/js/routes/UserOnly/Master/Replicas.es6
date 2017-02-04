import actions from 'src/actions'
import {ReplicaIcon} from 'src/components/bases/icons'
import Replicas from 'src/containers/Replicas'

const replicasRoute = {
  key: 'replicas',
  path: 'replicas',
  label: '共有リンク一覧',
  icon: ReplicaIcon,
  component: Replicas,
  onEnterActions: [
    actions.replicationLinks.fetchRequest,
  ],
}

export default replicasRoute
