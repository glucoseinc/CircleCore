import React, {Component, PropTypes} from 'react'

import FlatButton from 'material-ui/FlatButton'
import {GridList, GridTile} from 'material-ui/GridList'
import Toggle from 'material-ui/Toggle'
import {grey200, redA200} from 'material-ui/styles/colors'

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
    onDisplayNameTouchTap: PropTypes.func,
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
      onDisplayNameTouchTap,
    } = this.props
    const {
      autoUpdate,
      graphRange,
    } = this.state

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
      },

      toggleSection: {
        display: 'flex',
        justifyContent: 'flex-end',
      },
      toggle: {
        width: 'auto',
      },

      timeRangeSection: {
        marginTop: 8,
        display: 'flex',
        flexFlow: 'row nowrap',
        background: grey200,
      },
      timeRange: {
        borderBottomStyle: 'none',
      },
      timeRangeLanel: {
      },
      activeTimeRange: {
        borderBottomStyle: 'solid',
        borderBottomWidth: 2,
        borderBottomColor: redA200,
      },
      activeTimeRangeLabel: {
        color: redA200,
      },

      moduleCardList: {
        paddingTop: 12,
      },
      moduleCardTile: {
        padding: 4,
      },

    }

    return (
      <div style={style.root}>
        <div style={style.toggleSection}>
          <Toggle
            style={style.toggle}
            label="自動更新(1分)"
            toggled={autoUpdate}
            onToggle={() => this.setState({autoUpdate: !this.state.autoUpdate})}
          />
        </div>

        <div style={style.timeRangeSection}>
          {RANGES.map((range) =>
            <FlatButton
              key={range}
              style={graphRange === range ? style.activeTimeRange : style.timeRange}
              label={RANGE_LABELS[range]}
              labelStyle={graphRange === range ? style.activeTimeRangeLabel : style.timeRangeLabel}
              onTouchTap={() => this.setState({graphRange: range})}
            />
          )}
        </div>

        <GridList
          cols={cols}
          cellHeight="auto"
          padding={8}
          style={style.moduleCardList}
        >
          {modules.valueSeq().map((module) => (
            <GridTile
              key={module.uuid}
              style={style.moduleCardTile}
            >
              <ModuleCard
                module={module}
                autoUpdate={autoUpdate}
                graphRange={graphRange}
                onDisplayNameTouchTap={onDisplayNameTouchTap}
              />
            </GridTile>
          ))}
        </GridList>
      </div>
    )
  }
}

export default ModuleCards
