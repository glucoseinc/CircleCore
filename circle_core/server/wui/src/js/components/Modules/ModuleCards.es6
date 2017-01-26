import React, {Component, PropTypes} from 'react'

import FlatButton from 'material-ui/FlatButton'
import {Card, CardMedia, CardTitle} from 'material-ui/Card'
import Toggle from 'material-ui/Toggle'

import {colorUUID} from 'src/colors'
import {urls} from 'src/routes'

import CCLink from 'src/components/commons/CCLink'

import {ModuleGraph, RANGES, RANGE_LABELS} from './ModuleGraph'


/**
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
            <Card
              key={module.uuid}
              className="moduleCard"
            >
              <CardMedia>
                <ModuleGraph module={module} range={graphRange} autoUpdate={autoUpdate ? 60 : 0} />
              </CardMedia>
              <CardTitle
                title={
                  <CCLink url={urls.module} params={{moduleId: module.uuid}} style={{color: '#212121'}}>
                    {module.displayName}
                  </CCLink>}
                titleStyle={{
                  fontSize: '14px',
                  fotnWeight: 'bold',
                  lineHeight: '1.4',
                }}
                titleColor="#2121121"
                subtitle={module.uuid}
                subtitleColor={colorUUID}
                subtitleStyle={{
                  fontSize: '10px',
                }}
                style={{
                  padding: '8px 12px 0',
                }}
                />
            </Card>
          ))}
        </div>
      </div>
    )
  }
}

export default ModuleCards
