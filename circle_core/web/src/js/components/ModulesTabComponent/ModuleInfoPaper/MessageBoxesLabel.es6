import React, {Component, PropTypes} from 'react'

import {blue500} from 'material-ui/styles/colors'

import ComponentWithIcon from 'src/components/bases/ComponentWithIcon'
import {MessageBoxIcon} from 'src/components/bases/icons'


/**
 * MessageBoxリストラベル
 */
class MessageBoxesLabel extends Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
  }


  /**
   * @override
   */
  render() {
    const {
      module,
    } = this.props

    const style = {
      messageBoxes: {
        display: 'flex',
        flexFlow: 'row wrap',
        marginLeft: -16,
        lineHeight: 1,
      },
      messageBox: {
        paddingLeft: 16,
        fontSize: 14,
        fontWeight: 'bold',
        color: blue500,
      },
    }

    return (
      <ComponentWithIcon icon={MessageBoxIcon}>
        <div style={style.messageBoxes}>
          {module.messageBoxes.valueSeq().map((messageBox, index) =>
            <span key={index} style={style.messageBox}>
              {messageBox.label}
            </span>
          )}
        </div>
      </ComponentWithIcon>
    )
  }
}

export default MessageBoxesLabel
