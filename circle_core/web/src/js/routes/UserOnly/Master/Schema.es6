import actions from 'src/actions'
import Schema from 'src/containers/Schema'

const schemaRoute = {
  key: 'schema',
  path: 'schemas/:schemaId',
  label: 'メッセージスキーマ詳細',
  // icon: null,
  component: Schema,
  onEnterActions: [
    actions.schema.fetchRequest,
  ],
}

export default schemaRoute
