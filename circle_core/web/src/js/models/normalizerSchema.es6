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
  {
    schema: schema,
  },
  {
    idAttribute: 'uuid',
  }
)

const module = new normalizerSchema.Entity(
  'modules',
  {
    messageBoxes: [messageBox],
  },
  {
    idAttribute: 'uuid',
  }
)

// 循環参照yeah!
messageBox.define({module: module})

schema.define({
  modules: [module],
})

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
    // processStrategy: (entity) => ({
    //   uuid: entity.uuid,
    //   displayName: entity.displayName,
    //   ccInfos: entity.ccInfoUuids,
    //   messageBoxes: entity.messageBoxUuids,
    //   memo: entity.memo,
    //   link: entity.link,
    // }),
  }
)

const replicationMaster = new normalizerSchema.Entity(
  'replicationMasters',
  {},
  {
    idAttribute: 'id',
  }
)

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
