import actions from 'src/actions'
import {CoreIcon} from 'src/components/bases/icons'
import ReplicactionMasters from 'src/containers/ReplicationMasters'

const coresRoute = {
  key: 'replicationMasters',
  path: 'replication_masters/',
  label: '共有マスター一覧',
  icon: CoreIcon,
  component: ReplicactionMasters,
  onEnterActions: [
    actions.replicationMaster.fetchAllRequest,
  ],
}

export default coresRoute
