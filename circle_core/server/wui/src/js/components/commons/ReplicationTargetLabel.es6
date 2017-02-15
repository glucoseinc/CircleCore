import React, {Component, PropTypes} from 'react'
import {grey600} from 'material-ui/styles/colors'

import {ModuleIcon} from 'src/components/bases/icons'

const moduleColor = grey600


/**
 * ReplicationLinkターゲットラベル
 */
class ReplicationTargetLabel extends Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    messageBoxes: PropTypes.array.isRequired,
    rootStyle: PropTypes.object,
  }

  /**
   * @override
   */
  render() {
    const {
      messageBoxes,
      module,
    } = this.props

    const style = {
      root: {
        // display: 'flex',
        // flexFlow: 'row nowrap',
        // justifyContent: 'space-between',
        // width: '100%',
        // padding: 8,
        fontSize: 14,
        ...(this.props.rootStyle || {}),
      },
      displayName: {
        fontWeight: 'bold',
        color: moduleColor,
      },
      moduleIcon: {
        width: 16,
        height: 16,
        verticalAlign: 'text-bottom',
        marginRight: '0.2em',
      },
      messageBoxes: {
      },
      messageBoxDisplayName: {
        // color: grey600,
        fontSize: 12,
        marginRight: '1em',
      },
    }

    return (
      <div className="replcationLinks-row-targets" style={style.root}>
        <div style={style.displayName}>
          <ModuleIcon style={style.moduleIcon} color={moduleColor} />{module.displayName || '(no name)'}
        </div>
        <div className="replcationLinks-row-messageBoxes">
          {messageBoxes.map((box) => (
            <span
              key={box.uuid}
              style={style.messageBoxDisplayName}>
              {box.displayName || '(no name)'}
            </span>
          ))}
        </div>
      </div>
    )
  }
}

export default ReplicationTargetLabel
