import {GuestOnly} from 'src/containers/AuthDivider'

import OAuthAuthorize from './OAuthAuthorize'
import CheckingAuthCode from './CheckingAuthCode'

const guestOnlyRoute = {
  key: 'guestOnly',
  component: GuestOnly,
  childRoutes: [
    OAuthAuthorize,
    CheckingAuthCode,
  ],
}

export default guestOnlyRoute
