import PropTypes from 'prop-types'
import React from 'react'

import {grey300} from 'material-ui/styles/colors'

import ComponentWithIcon from 'src/components/bases/ComponentWithIcon'
import {MessageBoxIcon} from 'src/components/bases/icons'

import MessageBoxComponent from './MessageBoxComponent'


/**
 * MessageBoxリストラベル
 */
class MessageBoxesLabel extends React.Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    ccInfos: PropTypes.object.isRequired,
  }


  /**
   * @override
   */
  render() {
    const {
      module,
      ccInfos,
    } = this.props

    const style = {
      messageBoxes: {
        display: 'flex',
        flexFlow: 'column wrap',
      },
    }

    const masterCcInfo = ccInfos.get(module.ccUuid)

    return (
      <ComponentWithIcon icon={MessageBoxIcon}>
        <div style={style.messageBoxes}>
          {module.messageBoxes.valueSeq().map((messageBox, index) => (
            <MessageBoxComponent
              key={messageBox.uuid}
              messageBox={messageBox}
              ccInfos={ccInfos}
              masterCcInfo={masterCcInfo}
              backgroundColor={index % 2 ? null : grey300}
            />
          ))}
        </div>
      </ComponentWithIcon>
    )
  }
}

export default MessageBoxesLabel
