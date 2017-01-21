import Master from '../../../containers/Master'

import ChangeProfile from './ChangeProfile'
import Cores from './Cores'
import Dump from './Dump'
import Invitations from './Invitations'
import Logout from './Logout'
import Modules from './Modules'
import ModulesNew from './ModulesNew'
import Module from './Module'
import Replicas from './Replicas'
import Schemas from './Schemas'
import SchemasNew from './SchemasNew'
import Schema from './Schema'
import Setting from './Setting'
import Users from './Users'
import User from './User'


const master = {
  key: 'root',
  component: Master,
  childRoutes: [
    ChangeProfile,
    Cores,
    Dump,
    Invitations,
    Logout,
    Modules,
    ModulesNew,
    Module,
    Replicas,
    Schemas,
    SchemasNew,
    Schema,
    Setting,
    Users,
    User,
  ],
}

export default master
