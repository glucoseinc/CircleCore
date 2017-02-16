import actions from 'src/actions'
import Replica from 'src/containers/Replica'

const replicaRoute = {
  key: 'replica',
  path: 'replicas/:replicationLinkId',
  label: '共有リンク詳細',
  // icon: null,
  component: Replica,
  onEnterActions: [
    actions.replicationLink.fetchAllRequest,
  ],
}

export default replicaRoute
