import actions from 'src/actions'
import User from 'src/containers/User'

const userRoute = {
  key: 'user',
  path: 'users/:userId([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})',
  label: 'ユーザー詳細',
  // icon: null,
  component: User,
  onEnterActions: [
    actions.user.fetchRequest,
  ],
}

export default userRoute
