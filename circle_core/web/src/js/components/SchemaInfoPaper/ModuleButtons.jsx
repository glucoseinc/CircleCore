import PropTypes from 'prop-types'
import React from 'react'

import ComponentWithIcon from 'src/components/bases/ComponentWithIcon'
import {ModuleIcon} from 'src/components/bases/icons'

import ModuleButton from './ModuleButton'


/**
 * Moduleボタンリスト
 */
class ModuleButtons extends React.Component {
  static propTypes = {
    schema: PropTypes.object.isRequired,
    modules: PropTypes.object.isRequired,
    onClick: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      schema,
      modules,
      onClick,
    } = this.props

    const style = {
      modules: {
        display: 'flex',
        flexFlow: 'row wrap',
        lineHeight: 1,
        marginTop: -4,
      },
    }
    console.log(schema.modules, modules)
    return (
      <ComponentWithIcon icon={ModuleIcon}>
        <div style={style.modules}>
          {schema.modules.valueSeq().map((moduleId, index) => (
            <ModuleButton
              key={moduleId}
              module={modules.get(moduleId)}
              onClick={(onClick)}
            />
          ))}
        </div>
      </ComponentWithIcon>
    )
  }
}

export default ModuleButtons
