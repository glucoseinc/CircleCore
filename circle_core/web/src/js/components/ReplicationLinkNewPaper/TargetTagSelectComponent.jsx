import {List} from 'immutable'
import MenuItem from 'material-ui/MenuItem'
import SelectField from 'material-ui/SelectField'
import PropTypes from 'prop-types'
import React from 'react'

import ComponentWithIcon from 'src/components/bases/ComponentWithIcon'
import {ModuleIcon} from 'src/components/bases/icons'


/**
 * ReplicationLink対象選択コンポーネント(タイプ：タグ)
 */
class TargetTagSelectComponent extends React.Component {
  static propTypes = {
    replicationLink: PropTypes.object.isRequired,
    modules: PropTypes.object.isRequired,
    selectedModule: PropTypes.object.isRequired,
    onUpdate: PropTypes.func,
  }

  state = {
    selectedTag: null,
  }

  /**
   * @override
   */
  render() {
    const {
      selectedTag,
    } = this.state
    const {
      replicationLink,
      modules,
      selectedModule,
      onUpdate,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
      },
      tag: {
      },

      modules: {
        display: 'flex',
        flexFlow: 'row wrap',
      },
      module: {
        fontSize: 14,
        width: '50%',
      },

    }

    const filteredModules = modules.filter((module) => module.tags.includes(selectedTag))

    return (
      <div style={style.root}>
        <div style={style.tag}>
          <SelectField
            floatingLabelText="タグ"
            value={selectedTag}
            onChange={(e, i, v) => {
              const newTag = v
              this.setState({selectedTag: newTag})

              const messageBoxIds = modules.filter(
                (module) => module.tags.includes(newTag)
              ).reduce(
                (_messageBoxIds, module) => (
                  _messageBoxIds.concat(module.messageBoxes.map((messageBox) => messageBox.uuid))
                ),
                new List(),
              )

              onUpdate(replicationLink.updateMessageBoxes(messageBoxIds.toArray()))
            }}
          >
            {selectedModule.tags.valueSeq().map((tag) => (
              <MenuItem
                key={tag}
                value={tag}
                primaryText={tag}
              />
            ))}
          </SelectField>
        </div>
        <ComponentWithIcon icon={ModuleIcon}>
          <div style={style.modules}>
            {filteredModules.valueSeq().map((module) => (
              <div
                key={module.uuid}
                style={style.module}
              >
                {module.label}
              </div>
            ))}
          </div>
        </ComponentWithIcon>
      </div>
    )
  }
}


export default TargetTagSelectComponent
