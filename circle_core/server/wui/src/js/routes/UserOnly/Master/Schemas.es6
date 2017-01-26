import actions from 'src/actions'
import {SchemaIcon} from 'src/components/bases/icons'
import Schemas from 'src/containers/Schemas'

const schemasRoute = {
  key: 'schemas',
  path: 'schemas',
  label: 'メッセージスキーマ一覧',
  icon: SchemaIcon,
  component: Schemas,
  onEnterActions: [
    actions.schemas.fetchRequest,
  ],
}

export default schemasRoute
