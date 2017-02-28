import React, {Component, PropTypes} from 'react'

import TextField from 'material-ui/TextField'

import ComponentWithIconButton from 'src/components/bases/ComponentWithIconButton'
import {DeleteIcon} from 'src/components/bases/icons'


/**
* ModuleAttribute編集コンポーネント
*/
class ModuleAttributeEditComponent extends Component {
  static propTypes = {
    attribute: PropTypes.object.isRequired,
    onUpdate: PropTypes.func,
    onDeleteTouchTap: PropTypes.func,
    onNameChange: PropTypes.func,
    onValueChange: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      attribute,
      onUpdate,
      onDeleteTouchTap,
    } = this.props

    const style = {
      root: {
        alignItems: 'baseline',
      },
      children: {
        flexGrow: 0,
      },
      attributeName: {
      },
      attributeType: {
        paddingLeft: 16,
      },
    }
    return (
      <ComponentWithIconButton
        rootStyle={style.root}
        childrenStyle={style.children}
        icon={DeleteIcon}
        onIconButtonTouchTap={onDeleteTouchTap}
      >
        <TextField
          floatingLabelText="属性名"
          value={attribute.name}
          style={style.attributeName}
          onChange={(e, newValue) => onUpdate(attribute.updateName(newValue))}
        />
        <TextField
          floatingLabelText="属性値"
          value={attribute.value}
          style={style.attributeType}
          onChange={(e, newValue) => onUpdate(attribute.updateValue(newValue))}
        />
      </ComponentWithIconButton>
    )
  }
}


export default ModuleAttributeEditComponent
