import UserOnly from './UserOnly'
import GuestOnly from './GuestOnly'
import NotFound from './NotFound'

const rootRoute = {
  key: 'root',
  path: '/',
  childRoutes: [
    UserOnly,
    GuestOnly,
    NotFound,
  ],
}

export default rootRoute
