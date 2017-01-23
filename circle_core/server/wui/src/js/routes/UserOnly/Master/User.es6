import actions from '../../../actions'
import User from '../../../containers/User'

const userRoute = {
  key: 'user',
  path: 'users/:userId',
  label: 'ユーザー詳細',
  // icon: null,
  component: User,
  onEnterActions: [
    actions.users.fetchRequest,
  ],
}

export default userRoute
