import actions from 'src/actions'
import SchemasNew from 'src/containers/SchemasNew'

const schemasNewRoute = {
  key: 'schemasNew',
  path: 'schemas/new',
  query: {
    schema_id: ':schemaId',
  },
  label: 'メッセージスキーマ作成',
  // icon: null,
  component: SchemasNew,
  onEnterActions: [
    actions.schema.fetchAllRequest,
    actions.schemaPropertyType.fetchAllRequest,
  ],
}

export default schemasNewRoute
