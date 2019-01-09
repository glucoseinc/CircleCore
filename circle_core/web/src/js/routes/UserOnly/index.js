import {UserOnly} from 'src/containers/AuthDivider'

import Master from './Master'

const userOnlyRoute = {
  key: 'userOnly',
  component: UserOnly,
  childRoutes: [
    Master,
  ],
}

export default userOnlyRoute
