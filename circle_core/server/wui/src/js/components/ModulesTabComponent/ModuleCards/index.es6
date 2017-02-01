import React, {Component, PropTypes} from 'react'

import FlatButton from 'material-ui/FlatButton'
import Toggle from 'material-ui/Toggle'

import {RANGES, RANGE_LABELS} from 'src/components/commons/ModuleGraph'

import ModuleCard from './ModuleCard'


/**
 * Module一覧(カード)
 */
class ModuleCards extends Component {
  static propTypes = {
    cols: PropTypes.number,
    timeAxisUnit: PropTypes.number,
    modules: PropTypes.object.isRequired,
  }

  static defaultProps = {
    cols: 2,
  }

  /**
   * @constructor
   */
  constructor(...args) {
    super(...args)

    this.state = {
      autoUpdate: true,
      graphRange: RANGES[0],
    }
  }

  /**
   * @override
   */
  render() {
    const {
      cols,
      modules,
    } = this.props
    const {
      autoUpdate,
      graphRange,
    } = this.state

    return (
      <div className="moduleCardsTab">
        <div className="moduleCardsTab-timeRanges">
          {RANGES.map((r) => (
            <div
              key={r}
              className={`moduleCardsTab-timeRange ${graphRange === r ? 'is-active' : ''}`}
              >
              <FlatButton
                label={RANGE_LABELS[r]}
                onTouchTap={() => this.setState({graphRange: r})}
              />
            </div>
          ))}
        </div>

        <div className={`moduleCards moduleCards-col${cols}`}>

          <div className="moduleCards-toggle">
            <Toggle
              label="自動更新(1分)"
              toggled={autoUpdate}
              onToggle={() => this.setState({autoUpdate: !this.state.autoUpdate})}
            />
          </div>

          {modules.valueSeq().map((module) => (
            <ModuleCard
              key={module.uuid}
              module={module}
              autoUpdate={autoUpdate}
              graphRange={graphRange}
            />
          ))}
        </div>
      </div>
    )
  }
}

export default ModuleCards
