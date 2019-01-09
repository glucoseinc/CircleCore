import actions from 'src/actions'
import Replica from 'src/containers/Replica'

const replicaRoute = {
  key: 'replica',
  path: 'replicas/:replicationLinkId([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})',
  label: '共有リンク詳細',
  // icon: null,
  component: Replica,
  onEnterActions: [
    actions.replicationLink.fetchAllRequest,
  ],
}

export default replicaRoute
