import React, {Component, PropTypes} from 'react'

import ComponentWithIcon from 'src/components/bases/ComponentWithIcon'
import {ModuleIcon} from 'src/components/bases/icons'

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
      modules: {
        display: 'flex',
        flexFlow: 'row wrap',
        lineHeight: 1,
        marginTop: -4,
      },
    }

    return (
      <ComponentWithIcon icon={ModuleIcon}>
        <div style={style.modules}>
          {schema.modules.valueSeq().map((moduleId, index) =>
            <ModuleButton
              key={moduleId}
              module={modules.get(moduleId)}
              onTouchTap={(onTouchTap)}
            />
          )}
        </div>
      </ComponentWithIcon>
    )
  }
}

export default ModuleButtons
