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

const response = {
  schema,
  schemas: [schema],
  schemaPropertyTypes: [schemaPropertyType],
  module,
  modules: [module],
}

export default response
