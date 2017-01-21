import {UserOnly} from '../../containers/AuthDivider'

import Master from './Master'

const userOnlyRoute = {
  component: UserOnly,
  childRoutes: [
    Master,
  ],
}

export default userOnlyRoute
