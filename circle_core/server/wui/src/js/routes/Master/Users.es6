import User from '../../containers/User'
import Users from '../../containers/Users'

export default [
  {
    key: 'users',
    path: 'users/',
    label: 'ユーザー一覧',
    component: Users,
  },
  {
    key: 'user',
    path: 'users/:userId',
    label: 'ユーザー詳細',
    component: User,
  },
]
