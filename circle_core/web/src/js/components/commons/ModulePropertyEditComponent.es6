import React, {Component, PropTypes} from 'react'

import TextField from 'material-ui/TextField'

import ComponentWithIconButton from 'src/components/bases/ComponentWithIconButton'
import {DeleteIcon} from 'src/components/bases/icons'


/**
* ModuleProperty編集コンポーネント
*/
class ModulePropertyEditComponent extends Component {
  static propTypes = {
    property: PropTypes.object.isRequired,
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
      property,
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
          value={property.name}
          onChange={(e, newValue) => onUpdate(property.updateName(newValue))}
        />
        <TextField
          floatingLabelText="属性値"
          value={property.value}
          onChange={(e, newValue) => onUpdate(property.updateValue(newValue))}
        />
      </ComponentWithIconButton>
    )
  }
}


export default ModulePropertyEditComponent
