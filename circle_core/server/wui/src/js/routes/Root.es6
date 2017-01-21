import UserOnly from './UserOnly'
import GuestOnly from './GuestOnly'
import NotFound from './NotFound'

const rootRoute = {
  path: '/',
  childRoutes: [
    UserOnly,
    GuestOnly,
    NotFound,
  ],
}

export default rootRoute
