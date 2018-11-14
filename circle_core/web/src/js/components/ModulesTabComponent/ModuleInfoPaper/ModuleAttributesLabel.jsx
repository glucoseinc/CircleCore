import React, {Component, PropTypes} from 'react'

import ComponentWithIcon from 'src/components/bases/ComponentWithIcon'
import {AttributeIcon} from 'src/components/bases/icons'


/**
* ModuleAttributesラベルコンポーネント
*/
class ModuleAttributesLabel extends Component {
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
      attributes: {
        display: 'flex',
        flexFlow: 'row wrap',
        marginTop: -4,
        marginLeft: -16,
        fontSize: 14,
      },
      attribute: {
        paddingLeft: 16,
      },
    }

    return (
      <ComponentWithIcon icon={AttributeIcon}>
        <div style={style.attributes}>
          {module.attributes.valueSeq().map((attribute, index) =>
            <div key={index} style={style.attribute}>
              {attribute.name} : {attribute.value}
            </div>
          )}
        </div>
      </ComponentWithIcon>
    )
  }
}


export default ModuleAttributesLabel
