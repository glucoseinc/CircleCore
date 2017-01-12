import Master from '../../containers/Master'


const children = [
  'ChangeProfile',
  'Logout',
  'Modules',
  'ModulesNew',
  'Module',
  'Schemas',
  'SchemasNew',
  'Schema',
  'User',
  'Users',

  // 必ず最後
  'NotFound',
]

const masterRoute = {
  key: 'root',
  path: '/',
  component: Master,
  indexRoute: {component: require('./Modules').default.component},
  childRoutes: children.map((child) => require(`./${child}`).default),
}


export default masterRoute
