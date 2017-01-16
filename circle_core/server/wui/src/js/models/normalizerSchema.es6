import {schema as normalizerSchema} from 'normalizr'


const schema = new normalizerSchema.Entity(
  'schemas',
  {},
  {
    idAttribute: 'uuid',
  }
)

const module = new normalizerSchema.Entity(
  'modules',
  {
    messageBoxes: [{
      schema: schema,
    }],
  },
  {
    idAttribute: 'uuid',
  }
)

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


const response = {
  invitation,
  invitations: [invitation],
  schema,
  schemas: [schema],
  schemaPropertyTypes: [schemaPropertyType],
  module,
  modules: [module],
  users: [user],
}

export default response
