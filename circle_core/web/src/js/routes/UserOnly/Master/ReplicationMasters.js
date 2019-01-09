import actions from 'src/actions'
import {CoreIcon} from 'src/components/bases/icons'
import ReplicationMasters from 'src/containers/ReplicationMasters'

const replicationMastersRoute = {
  key: 'replicationMasters',
  path: 'replication_masters/',
  label: '共有マスター一覧',
  icon: CoreIcon,
  component: ReplicationMasters,
  onEnterActions: [
    actions.replicationMaster.fetchAllRequest,
  ],
}

export default replicationMastersRoute
