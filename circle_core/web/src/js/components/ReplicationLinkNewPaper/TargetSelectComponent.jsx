import PropTypes from 'prop-types'
import React from 'react'

import {RadioButton, RadioButtonGroup} from 'material-ui/RadioButton'

import TargetMessageBoxSelectComponent from './TargetMessageBoxSelectComponent'
import TargetTagSelectComponent from './TargetTagSelectComponent'


/**
 * ReplicationLink対象選択コンポーネント
 */
class TargetSelectComponent extends React.Component {
  static propTypes = {
    replicationLink: PropTypes.object.isRequired,
    modules: PropTypes.object.isRequired,
    selectedModule: PropTypes.object,
    onUpdate: PropTypes.func,
  }

  static targetType = {
    module: 'MODULE',
    tag: 'TAG',
  }

  state = {
    targetType: TargetSelectComponent.targetType.module,
  }

  /**
   * @override
   */
  render() {
    const {
      targetType,
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

      switches: {
        paddingTop: 8,
      },
      targetTypes: {
        display: 'flex',
        flexFlow: 'row nowrap',
      },
      targetType: {
        width: 160,
      },
      target: {
        paddingTop: 8,
        paddingLeft: 40,
      },
    }

    const targetComponent = targetType === TargetSelectComponent.targetType.module ? (
      <TargetMessageBoxSelectComponent
        replicationLink={replicationLink}
        selectedModule={selectedModule}
        onUpdate={onUpdate}
      />
    ) : (
      <TargetTagSelectComponent
        replicationLink={replicationLink}
        modules={modules}
        selectedModule={selectedModule}
        onUpdate={onUpdate}
      />
    )

    return (
      <div style={style.root}>
        <div style={style.switches}>
          <RadioButtonGroup
            name="targetType"
            valueSelected={targetType}
            style={style.targetTypes}
            onChange={(e, v) => {
              this.setState({targetType: v})
              onUpdate(replicationLink.clearMessageBoxes())
            }}
          >
            <RadioButton
              value={TargetSelectComponent.targetType.module}
              label="モジュール"
              style={style.targetType}
            />
            <RadioButton
              value={TargetSelectComponent.targetType.tag}
              label="タグ"
              style={style.targetType}
            />
          </RadioButtonGroup>
        </div>
        <div style={style.target}>
          {targetComponent}
        </div>
      </div>
    )
  }
}


export default TargetSelectComponent
