import actions from 'src/actions'
import {CoreIcon} from 'src/components/bases/icons'
import ReplicationMasters from 'src/containers/ReplicationMasters'
import ReplicationMasterNew from 'src/containers/ReplicationMasterNew'

export default [{
  key: 'replicationMasters',
  path: 'replication_masters/',
  label: '共有マスター一覧',
  icon: CoreIcon,
  component: ReplicationMasters,
  onEnterActions: [
    actions.replicationMaster.fetchAllRequest,
  ],
}, {
  key: 'replicationMasterNew',
  path: 'replication_masters/new',
  label: '共有マスター追加',
  icon: CoreIcon,
  component: ReplicationMasterNew,
}]
