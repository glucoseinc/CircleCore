import actions from 'src/actions'
import User from 'src/containers/User'

const userRoute = {
  key: 'user',
  path: 'users/:userId',
  label: 'ユーザー詳細',
  // icon: null,
  component: User,
  onEnterActions: [
    actions.user.fetchRequest,
  ],
}

export default userRoute
