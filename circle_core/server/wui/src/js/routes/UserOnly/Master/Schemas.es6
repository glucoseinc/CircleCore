import ActionReceipt from 'material-ui/svg-icons/action/receipt'
import actions from '../../../actions'
import Schemas from '../../../containers/Schemas'

const schemasRoute = {
  key: 'schemas',
  path: 'schemas',
  label: 'メッセージスキーマ一覧',
  icon: ActionReceipt,
  component: Schemas,
  onEnterActions: [
    actions.schemas.fetchRequest,
  ],
}

export default schemasRoute
