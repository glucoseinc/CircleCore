import actions from 'src/actions'
import {ReplicationLinkIcon} from 'src/components/bases/icons'
import Replicas from 'src/containers/Replicas'

const replicasRoute = {
  key: 'replicas',
  path: 'replicas/',
  label: '共有リンク一覧',
  icon: ReplicationLinkIcon,
  component: Replicas,
  onEnterActions: [
    actions.replicationLink.fetchAllRequest,
  ],
}

export default replicasRoute
