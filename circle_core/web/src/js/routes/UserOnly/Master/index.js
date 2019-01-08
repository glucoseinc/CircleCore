import Master from 'src/containers/Master'

import ChangeProfile from './ChangeProfile'
import Invitations from './Invitations'
import Logout from './Logout'
import Modules from './Modules'
import ModulesNew from './ModulesNew'
import Module from './Module'
import Replica from './Replica'
import Replicas from './Replicas'
import ReplicasNew from './ReplicasNew'
import ReplicationMasters from './ReplicationMasters'
import ReplicationMastersNew from './ReplicationMastersNew'
import Schemas from './Schemas'
import SchemasNew from './SchemasNew'
import Schema from './Schema'
import Setting from './Setting'
import Users from './Users'
import User from './User'


const masterRoute = {
  key: 'master',
  component: Master,
  childRoutes: [
    ChangeProfile,
    Invitations,
    Logout,
    Module,
    Modules,
    ModulesNew,
    Replica,
    Replicas,
    ReplicasNew,
    ReplicationMasters,
    ReplicationMastersNew,
    Schema,
    Schemas,
    SchemasNew,
    Setting,
    User,
    Users,
  ],
}

export default masterRoute
