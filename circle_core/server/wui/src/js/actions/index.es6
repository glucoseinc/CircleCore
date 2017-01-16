let actions = {}
let actionTypes = {}


// load action groups
const groupNames = [
  'auth',
  'invitations',
  'location',
  'misc',
  'module',
  'modules',
  'schema',
  'schemas',
  'schemaPropertyTypes',
  'shareLinks',
  'user',
  'users',
]
groupNames.forEach((group) => {
  let mod = require(`./${group}`)

  actions[group] = mod.default
  actionTypes[group] = mod.actionTypes
})

export {actions as default, actionTypes}
