import React, {Component, PropTypes} from 'react'

import AddFlatButton from 'src/components/commons/AddFlatButton'
import ModulePropertyEditComponent from 'src/components/commons/ModulePropertyEditComponent'


/**
* ModuleProperty編集コンポーネント
*/
class ModulePropertieEditComponent extends Component {
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

      properties: {
        marginTop: -8,
      },
      propertyBlock: {
        paddingTop: 8,
      },

      actionsBlock: {
        paddingTop: 16,
      },
    }

    return (
      <div style={style.root}>
        <div style={style.properties}>
          {module.properties.valueSeq().map((property, index) =>
            <div key={index} style={style.propertyBlock}>
              <ModulePropertyEditComponent
                property={property}
                onUpdate={(newProperty) => onUpdate(index, newProperty)}
                onDeleteTouchTap={() => onDeleteTouchTap(index)}
              />
            </div>
          )}
        </div>
        <div style={style.actionsBlock}>
          <AddFlatButton
            label="プロパティを追加する"
            onTouchTap={onAddTouchTap}
          />
        </div>
      </div>
    )
  }
}


export default ModulePropertieEditComponent
