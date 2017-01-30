import React, {Component, PropTypes} from 'react'

import {grey500} from 'material-ui/styles/colors'
import ActionSettingsInputComponent from 'material-ui/svg-icons/action/settings-input-component'

import ModuleButton from './ModuleButton'


/**
 * Moduleボタンリスト
 */
class ModuleButtons extends Component {
  static propTypes = {
    schema: PropTypes.object.isRequired,
    modules: PropTypes.object.isRequired,
    onTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      schema,
      modules,
      onTouchTap,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'row nowrap',
        alignItems: 'center',
        lineHeight: 1,
      },
      icon: {
        width: 16,
        height: 16,
      },
      modules: {
        flexGrow: 1,
        fontSize: 14,
      },
    }

    return (
      <div
        style={style.root}
      >
        <ActionSettingsInputComponent style={style.icon} color={grey500}/>
        <div style={style.modules} onTouchTap={(e) => e.stopPropagation()}>
          {schema.modules.valueSeq().map((moduleId, index) => {
            const module = modules.get(moduleId)
            return (
              <ModuleButton
                key={moduleId}
                module={module}
                onTouchTap={(onTouchTap)}
              />
            )
          })}
        </div>
      </div>
    )
  }
}

export default ModuleButtons
