import actions from 'src/actions'
import SchemasNew from 'src/containers/SchemasNew'

const schemasNewRoute = {
  key: 'schemasNew',
  path: 'schemas/new',
  label: 'メッセージスキーマ作成',
  // icon: null,
  component: SchemasNew,
  onEnterActions: [
    actions.schemaPropertyType.fetchAllRequest,
  ],
}

export default schemasNewRoute
