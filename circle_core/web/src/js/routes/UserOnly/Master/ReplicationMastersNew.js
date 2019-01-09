import {CoreIcon} from 'src/components/bases/icons'
import ReplicationMasterNew from 'src/containers/ReplicationMasterNew'

const replicationMasterNewRoute = {
  key: 'replicationMasterNew',
  path: 'replication_masters/new',
  label: '共有マスター追加',
  icon: CoreIcon,
  component: ReplicationMasterNew,
}

export default replicationMasterNewRoute
