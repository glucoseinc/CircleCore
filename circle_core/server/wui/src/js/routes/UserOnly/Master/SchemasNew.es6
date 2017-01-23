import actions from '../../../actions'
import SchemasNew from '../../../containers/SchemasNew'

const schemasNewRoute = {
  key: 'schemasNew',
  path: 'schemas/new',
  label: 'メッセージスキーマ作成',
  // icon: null,
  component: SchemasNew,
  onEnterActions: [
    actions.schema.createInit,
    actions.schemaPropertyTypes.fetchRequest,
  ],
}

export default schemasNewRoute
