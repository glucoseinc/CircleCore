import React, {Component, PropTypes} from 'react'

import AddFlatButton from 'src/components/commons/AddFlatButton'
import ModuleAttributeEditComponent from 'src/components/commons/ModuleAttributeEditComponent'


/**
* ModuleAttribute編集コンポーネント
*/
class ModuleAttributesEditComponent extends Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
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

    return (
      <div style={style.root}>
        <div style={style.attributes}>
          {module.attributes.valueSeq().map((attribute, index) =>
            <div key={index} style={style.attributeBlock}>
              <ModuleAttributeEditComponent
                attribute={attribute}
                onUpdate={(newAttribute) => onUpdate(index, newAttribute)}
                onDeleteTouchTap={() => onDeleteTouchTap(index)}
              />
            </div>
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
