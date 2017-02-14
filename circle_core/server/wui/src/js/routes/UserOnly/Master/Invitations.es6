import actions from 'src/actions'
import {InvitationIcon} from 'src/components/bases/icons'
import Invitations from 'src/containers/Invitations'

const invitationsRoute = {
  key: 'invitations',
  path: 'invitations',
  label: '招待リンク一覧',
  icon: InvitationIcon,
  component: Invitations,
  onEnterActions: [
    actions.invitation.fetchAllRequest,
  ],
}

export default invitationsRoute
