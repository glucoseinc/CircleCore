import ActionExitToApp from 'material-ui/svg-icons/action/exit-to-app'
import Logout from '../../containers/Logout'

const logoutRoute = {
  key: 'logout',
  path: 'logout',
  label: 'ログアウト',
  icon: ActionExitToApp,
  component: Logout,
}

export default logoutRoute
