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
]

const pages = [].concat(...children.map((child) => {
  let routes = require(`./${child}`).default
  if(!Array.isArray(routes))
    routes = Array(routes)
  return routes
}))

export default pages
