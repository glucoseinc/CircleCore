import React, {Component, PropTypes} from 'react'

import {grey300, white} from 'material-ui/styles/colors'

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

    const targetModules = modules.map((module) => {
      const filteredMessageBoxes = module.messageBoxes.filter((messageBox) => {
        return replicationLink.messageBoxes.includes(messageBox.uuid)
      })
      return module.updateMessageBoxes(filteredMessageBoxes)
    }).filter((module) => module.messageBoxes.size > 0)

    return (
      <ComponentWithIcon icon={ReplicationTargetIcon}>
        {targetModules.valueSeq().map((module, index) =>
          <ReplicationTargetLabel
            key={module.uuid}
            module={module}
            rootStyle={{
              backgroundColor: index % 2 ? white :grey300,
            }}
          />
        )}
      </ComponentWithIcon>
    )
  }
}

export default ReplicationTargetsLabel
