import PropTypes from 'prop-types'
import React from 'react'

import AddFlatButton from 'src/components/commons/AddFlatButton'
import ModuleAttributeEditComponent from 'src/components/commons/ModuleAttributeEditComponent'


/**
* ModuleAttribute編集コンポーネント
*/
class ModuleAttributesEditComponent extends React.Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    nameSuggestions: PropTypes.array,
    valueSuggestions: PropTypes.array,
    onUpdate: PropTypes.func,
    onDeleteTouchTap: PropTypes.func,
    onAddTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      module,
      nameSuggestions = [],
      valueSuggestions = [],
      onUpdate,
      onDeleteTouchTap,
      onAddTouchTap,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
        width: '100%',
      },

      attributes: {
        marginTop: -8,
      },
      attributeBlock: {
        paddingTop: 8,
      },

      actionsBlock: {
        paddingTop: 16,
      },
    }

    const optimizedNameSuggestions = nameSuggestions.filter(
      (suggestion) => !module.attributes.map((attribute) => attribute.name).includes(suggestion)
    )

    const optimizedValueSuggestions = valueSuggestions.filter(
      (suggestion) => !module.attributes.map((attribute) => attribute.value).includes(suggestion)
    )

    return (
      <div style={style.root}>
        <div style={style.attributes}>
          {module.attributes.valueSeq().map((attribute, index) =>
            (<div key={index} style={style.attributeBlock}>
              <ModuleAttributeEditComponent
                attribute={attribute}
                nameSuggestions={optimizedNameSuggestions}
                valueSuggestions={optimizedValueSuggestions}
                onUpdate={(newAttribute) => onUpdate(index, newAttribute)}
                onDeleteTouchTap={() => onDeleteTouchTap(index)}
              />
            </div>)
          )}
        </div>
        <div style={style.actionsBlock}>
          <AddFlatButton
            label="属性を追加する"
            onTouchTap={onAddTouchTap}
          />
        </div>
      </div>
    )
  }
}


export default ModuleAttributesEditComponent
