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
    messageBoxes: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      replicationLink,
      messageBoxes,
    } = this.props

    const targetBoxes = replicationLink.messageBoxes.map((boxUuid) => messageBoxes.get(boxUuid))
    // const targetModules = modules.map((module) => {
    //   const filteredMessageBoxes = module.messageBoxes.filter((messageBox) => {
    //     return replicationLink.messageBoxes.includes(messageBox.uuid)
    //   })
    //   return module.updateMessageBoxes(filteredMessageBoxes)
    // }).filter((module) => module.messageBoxes.size > 0)

    return (
      <ComponentWithIcon icon={ReplicationTargetIcon}>
        {targetBoxes.map((messageBox, index) =>
          <ReplicationTargetLabel
            key={messageBox.uuid}
            messageBox={messageBox}
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
