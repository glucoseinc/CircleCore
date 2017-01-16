import Schema from '../../containers/Schema'

const schemaRoute = {
  key: 'schema',
  path: 'schemas/:schemaId',
  label: 'メッセージスキーマ詳細',
  component: Schema,
}

export default schemaRoute
