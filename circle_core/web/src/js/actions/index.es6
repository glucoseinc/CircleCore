export {actionTypePrefix} from './utils'

let actions = {}
let actionTypes = {}


// load action groups
const groupNames = [
  'auth',
  'ccInfo',
  'error',
  'invitation',
  'module',
  'page',
  'replicationLink',
  'schema',
  'schemaPropertyType',
  'user',
]
groupNames.forEach((group) => {
  let mod = require(`./${group}`)

  actions[group] = mod.default
  actionTypes[group] = mod.actionTypes
})

export {actions as default, actionTypes}
