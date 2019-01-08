import actions from 'src/actions'
import Schema from 'src/containers/Schema'

const schemaRoute = {
  key: 'schema',
  path: 'schemas/:schemaId([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})',
  label: 'メッセージスキーマ詳細',
  // icon: null,
  component: Schema,
  onEnterActions: [
    actions.schema.fetchRequest,
  ],
}

export default schemaRoute
