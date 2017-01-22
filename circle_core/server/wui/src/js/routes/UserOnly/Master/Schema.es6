import actions from '../../../actions'
import Schema from '../../../containers/Schema'

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
