import actions from 'src/actions'
import ReplicasNew from 'src/containers/ReplicasNew'

const replicasNewRoute = {
  key: 'replicasNew',
  path: 'replicas/new',
  query: {
    module_id: ':moduleId',
  },
  label: '共有リンク作成',
  // icon: null,
  component: ReplicasNew,
  onEnterActions: [
    actions.modules.fetchRequest,
  ],
}

export default replicasNewRoute
