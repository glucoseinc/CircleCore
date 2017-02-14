import actions from 'src/actions'
import {SettingIcon} from 'src/components/bases/icons'
import Setting from 'src/containers/Setting'

const settingRoute = {
  key: 'setting',
  path: 'setting',
  label: 'CircleCore情報変更',
  icon: SettingIcon,
  component: Setting,
  onEnterActions: [
    actions.ccInfo.fetchMyselfRequest,
  ],
}

export default settingRoute
