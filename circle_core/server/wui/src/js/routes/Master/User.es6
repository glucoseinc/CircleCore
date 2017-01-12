import User from '../../containers/User'

const userRoute = {
  key: 'user',
  path: 'users/:userId',
  label: 'ユーザー詳細',
  component: User,
}

export default userRoute
