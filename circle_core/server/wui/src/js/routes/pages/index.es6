const children = [
  'ChangeProfile',
  'Cores',
  'Dump',
  'Logout',
  'Modules',
  'ModulesNew',
  'Module',
  'Replicas',
  'Schemas',
  'SchemasNew',
  'Schema',
  'Setting',
  'Users',
]

const pages = [].concat(...children.map((child) => {
  let routes = require(`./${child}`).default
  if(!Array.isArray(routes))
    routes = Array(routes)
  return routes
}))

export default pages
