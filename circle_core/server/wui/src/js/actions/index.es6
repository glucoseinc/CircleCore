let actions = {}
let actionTypes = {}


// load action groups
const groupNames = [
  'auth',
  'ccInfos',
  'invitations',
  'misc',
  'module',
  'modules',
  'page',
  'replicationLinks',
  'schema',
  'schemaPropertyTypes',
  'user',
]
groupNames.forEach((group) => {
  let mod = require(`./${group}`)

  actions[group] = mod.default
  actionTypes[group] = mod.actionTypes
})

export {actions as default, actionTypes}
