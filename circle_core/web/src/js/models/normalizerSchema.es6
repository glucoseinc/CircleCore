import {schema as normalizerSchema} from 'normalizr'


const schema = new normalizerSchema.Entity(
  'schemas',
  {},
  {
    idAttribute: 'uuid',
  }
)

const messageBox = new normalizerSchema.Entity(
  'messageBoxes',
  {},
  {
    idAttribute: 'uuid',
  }
)

const module = new normalizerSchema.Entity(
  'modules',
  {},
  {
    idAttribute: 'uuid',
  }
)

const schemaPropertyType = new normalizerSchema.Entity(
  'schemaPropertyTypes',
  {},
  {
    idAttribute: 'name',
  }
)

const user = new normalizerSchema.Entity(
  'users',
  {},
  {
    idAttribute: 'uuid',
  }
)

const invitation = new normalizerSchema.Entity(
  'invitations',
  {},
  {
    idAttribute: 'uuid',
  }
)

const ccInfo = new normalizerSchema.Entity(
  'ccInfos',
  {},
  {
    idAttribute: 'uuid',
  }
)

const replicationLink = new normalizerSchema.Entity(
  'replicationLinks',
  {
    messageBoxes: [messageBox],
    slaves: [ccInfo],
  },
  {
    idAttribute: 'uuid',
  }
)

const replicationMaster = new normalizerSchema.Entity(
  'replicationMasters',
  {},
  {
    idAttribute: 'id',
  }
)

schema.define({
  modules: [module],
})

messageBox.define({
  schema: schema,
  module: module,
  slaveCcInfos: [ccInfo],
})

module.define({
  messageBoxes: [messageBox],
  ccInfo: ccInfo,
})

const response = {
  ccInfo,
  ccInfos: [ccInfo],
  invitation,
  invitations: [invitation],
  replicationLink,
  replicationLinks: [replicationLink],
  schema,
  schemas: [schema],
  schemaPropertyTypes: [schemaPropertyType],
  module,
  modules: [module],
  user,
  users: [user],
  replicationMaster,
  replicationMasters: [replicationMaster],
}

export default response
