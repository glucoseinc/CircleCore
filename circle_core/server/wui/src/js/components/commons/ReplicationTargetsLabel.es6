import React, {Component, PropTypes} from 'react'

import ComponentWithIcon from 'src/components/bases/ComponentWithIcon'
import {ReplicationTargetIcon} from 'src/components/bases/icons'
import ReplicationTargetLabel from 'src/components/commons/ReplicationTargetLabel'


/**
 * ReplicationLinkターゲットリストラベル
 */
class ReplicationTargetsLabel extends Component {
  static propTypes = {
    replicationLink: PropTypes.object.isRequired,
    modules: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      replicationLink,
      modules,
    } = this.props

    // sort boxes by module
    const boxesByModules = replicationLink.messageBoxes.reduce((map, box) => {
      if(!map.hasOwnProperty(box.module))
        map[box.module] = []
      map[box.module].push(box)
      return map
    }, {})

    return (
      <ComponentWithIcon icon={ReplicationTargetIcon}>
        {Object.keys(boxesByModules).map((moduleUuid, index) => {
          const module = modules.get(moduleUuid)
          const boxes = boxesByModules[moduleUuid]
          return (
            <ReplicationTargetLabel
              key={module.uuid}
              module={module}
              messageBoxes={boxes}
              rootStyle={{
                marginTop: index > 0 ? 8 : 0,
              }}
            />
          )
        })}
      </ComponentWithIcon>
    )
  }
}

export default ReplicationTargetsLabel
