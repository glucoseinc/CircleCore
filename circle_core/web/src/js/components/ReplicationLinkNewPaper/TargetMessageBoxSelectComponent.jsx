import PropTypes from 'prop-types'
import React from 'react'

import Checkbox from 'material-ui/Checkbox'


/**
 * ReplicationLink対象選択コンポーネント(タイプ：モジュール)
 */
class TargetMessageBoxSelectComponent extends React.Component {
  static propTypes = {
    replicationLink: PropTypes.object.isRequired,
    selectedModule: PropTypes.object.isRequired,
    onUpdate: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      replicationLink,
      selectedModule,
      onUpdate,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
      },
      label: {
        fontSize: 14,
        fontWeight: 'bold',
        lineHeight: 1,
      },

      selects: {
        display: 'flex',
        flexFlow: 'column nowrap',
        paddingTop: 8,
      },
      selectLabel: {
        fontSize: 14,
      },
      messageBoxes: {
        display: 'flex',
        flexFlow: 'row wrap',
      },
      messageBox: {
        width: '50%',
      },
    }

    const messageBoxIds = selectedModule.messageBoxes.map((messageBox) => messageBox.uuid)

    return (
      <div style={style.root}>
        <div style={style.label}>
          {selectedModule.label}
        </div>
        <div style={style.selects}>
          <Checkbox
            checked={replicationLink.messageBoxes.toSet().equals(messageBoxIds.toSet())}
            label="全てを選択"
            labelStyle={style.selectLabel}
            onCheck={(e, isInputChecked) => onUpdate(
              isInputChecked ? replicationLink.updateMessageBoxes(messageBoxIds.toArray())
                : replicationLink.clearMessageBoxes()
            )}
          />
          <div style={style.messageBoxes}>
            {selectedModule.messageBoxes.valueSeq().map((messageBox) => (
              <Checkbox
                key={messageBox.uuid}
                checked={replicationLink.messageBoxes.includes(messageBox.uuid)}
                label={messageBox.label}
                style={style.messageBox}
                labelStyle={style.selectLabel}
                onCheck={(e, isInputChecked) => onUpdate(
                  isInputChecked ? replicationLink.addMessageBox(messageBox.uuid)
                    : replicationLink.deleteMessageBox(messageBox.uuid)
                )}
              />
            ))}
          </div>
        </div>
      </div>
    )
  }
}


export default TargetMessageBoxSelectComponent
