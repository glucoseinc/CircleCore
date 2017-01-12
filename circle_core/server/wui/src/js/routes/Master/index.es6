import Master from '../../containers/Master'


const children = [
  // 認証、自分関連
  'ChangeProfile',
  'Logout',

  'Modules',
  'ModulesNew',
  'Module',
  'Schemas',
  'SchemasNew',
  'Schema',
  'Users',
  'NotFound',
]
console.log(children.map((child) => require(`./${child}`).default))

const masterRoute = {
  key: 'root',
  path: '/',
  component: Master,
  indexRoute: {component: require('./Modules').default.component},
  childRoutes: children.map((child) => require(`./${child}`).default),
}

export default masterRoute
