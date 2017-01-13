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
  'Users',

  // 必ず最後
  'NotFound',
]

const masterRoute = {
  key: 'root',
  path: '/',
  component: Master,
  indexRoute: {component: require('./Modules').default.component},
  childRoutes: [].concat(...children.map((child) => {
    let routes = require(`./${child}`).default
    if(!Array.isArray(routes))
      routes = Array(routes)
    return routes
  })),
}

export default masterRoute
