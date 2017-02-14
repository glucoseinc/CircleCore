import actions from 'src/actions'
import {UserIcon} from 'src/components/bases/icons'
import Users from 'src/containers/Users'

const usersRoute = {
  key: 'users',
  path: 'users',
  label: 'ユーザー一覧',
  icon: UserIcon,
  component: Users,
  onEnterActions: [
    actions.user.fetchAllRequest,
  ],
}

export default usersRoute
