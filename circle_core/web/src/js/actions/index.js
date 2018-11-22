export {actionTypePrefix} from './utils'

const actions = {}
const actionTypes = {}


// load action groups
const groupNames = [
  'auth',
  'ccInfo',
  'error',
  'invitation',
  'module',
  'page',
  'replicationLink',
  'replicationMaster',
  'schema',
  'schemaPropertyType',
  'user',
]
groupNames.forEach((group) => {
  const mod = require(`./${group}`)

  actions[group] = mod.default
  actionTypes[group] = mod.actionTypes
})

export {actions as default, actionTypes}
