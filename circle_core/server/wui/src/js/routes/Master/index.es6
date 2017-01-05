import Master from '../../containers/Master'

import Modules from './Modules'
import ModulesNew from './ModulesNew'
import Module from './Module'
import Schemas from './Schemas'
import SchemasNew from './SchemasNew'
import Schema from './Schema'
import NotFound from './NotFound'

const masterRoute = {
  key: 'root',
  path: '/',
  component: Master,
  indexRoute: {component: Modules.component},
  childRoutes: [
    Modules,
    ModulesNew,
    Module,
    Schemas,
    SchemasNew,
    Schema,
    NotFound,
  ],
}

export default masterRoute
