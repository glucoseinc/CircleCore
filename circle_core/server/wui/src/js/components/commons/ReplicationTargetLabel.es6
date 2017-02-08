import React, {Component, PropTypes} from 'react'
import {grey600} from 'material-ui/styles/colors'


/**
 * ReplicationLinkターゲットラベル
 */
class ReplicationTargetLabel extends Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    rootStyle: PropTypes.object,
  }


  /**
   * @override
   */
  render() {
    const {
      module,
      rootStyle = {},
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'row nowrap',
        justifyContent: 'space-between',
        width: '100%',
        padding: 8,
        fontSize: 14,
      },
      displayName: {
      },
      messageBoxes: {
      },
      messageBoxDisplayName: {
        color: grey600,
      },
    }

    const mergedRootStyle = {
      ...style.root,
      ...rootStyle,
    }

    return (
      <div style={mergedRootStyle}>
        <div style={style.displayName}>
          {module.displayName || '(no name)'}
        </div>
        <div style={style.messageBoxes}>
          {module.messageBoxes.valueSeq().map((messageBox) =>
            <div key={messageBox.uuid} style={style.messageBoxDisplayName}>
              {messageBox.displayName || '(no name)'}
            </div>
          )}
        </div>
      </div>
    )
  }
}

export default ReplicationTargetLabel
