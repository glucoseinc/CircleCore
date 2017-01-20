const children = [
  'ChangeProfile',
  'Cores',
  'Dump',
  'Invitations',
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
  'User',
]

const pages = [].concat(...children.map((child) => {
  let routes = require(`./${child}`).default
  if(!Array.isArray(routes))
    routes = Array(routes)
  return routes
}))

export default pages

export const defaultPage = require('./Modules').default
