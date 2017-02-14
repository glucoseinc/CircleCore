import actions from 'src/actions'
import {ChangeProfileIcon} from 'src/components/bases/icons'
import ChangeProfile from 'src/containers/ChangeProfile'

const changeProfileRoute = {
  key: 'changeProfile',
  path: 'changeProfile',
  label: 'プロフィール変更',
  icon: ChangeProfileIcon,
  component: ChangeProfile,
  onEnterActions: [
    actions.user.fetchMyselfRequest,
  ],
}

export default changeProfileRoute
