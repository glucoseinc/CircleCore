import PropTypes from 'prop-types'
import React from 'react'

import AutoComplete from 'material-ui/AutoComplete'

import ComponentWithIconButton from 'src/components/bases/ComponentWithIconButton'
import {DeleteIcon} from 'src/components/bases/icons'


/**
* ModuleAttribute編集コンポーネント
*/
class ModuleAttributeEditComponent extends React.Component {
  static propTypes = {
    attribute: PropTypes.object.isRequired,
    nameSuggestions: PropTypes.array,
    valueSuggestions: PropTypes.array,
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
      nameSuggestions = [],
      valueSuggestions = [],
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
        <AutoComplete
          floatingLabelText="属性名"
          dataSource={nameSuggestions}
          searchText={attribute.name}
          style={style.attributeName}
          onUpdateInput={(newValue) => onUpdate(attribute.updateName(newValue))}
        />
        <AutoComplete
          floatingLabelText="属性値"
          dataSource={valueSuggestions}
          value={attribute.value}
          style={style.attributeType}
          onUpdateInput={(newValue) => onUpdate(attribute.updateValue(newValue))}
        />
      </ComponentWithIconButton>
    )
  }
}


export default ModuleAttributeEditComponent
