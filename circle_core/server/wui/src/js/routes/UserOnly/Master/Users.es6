import ActionSupervisorAccount from 'material-ui/svg-icons/action/supervisor-account'
import actions from '../../../actions'
import Users from '../../../containers/Users'

const usersRoute = {
  key: 'users',
  path: 'users/',
  label: 'ユーザー一覧',
  icon: ActionSupervisorAccount,
  component: Users,
  onEnterActions: [
    actions.users.fetchRequest,
  ],
}

export default usersRoute