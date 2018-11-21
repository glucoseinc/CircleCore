import PropTypes from 'prop-types'
import React from 'react'

import {GridList, GridTile} from 'material-ui/GridList'
import Toggle from 'material-ui/Toggle'

import {RANGES} from 'src/components/commons/ModuleGraph'
import ModuleGraphTimeRange from 'src/components/commons/ModuleGraphTimeRange'

import ModuleCard from './ModuleCard'


/**
 * Module一覧(カード)
 */
class ModuleCards extends React.Component {
  static propTypes = {
    cols: PropTypes.number,
    timeAxisUnit: PropTypes.number,
    modules: PropTypes.object.isRequired,
    onDisplayNameClick: PropTypes.func,
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
      onDisplayNameClick,
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

        <ModuleGraphTimeRange
          activeTimeRange={graphRange}
          style={style.timeRangeSection}
          onClick={(range) => this.setState({graphRange: range})}
        />

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
                onDisplayNameClick={onDisplayNameClick}
              />
            </GridTile>
          ))}
        </GridList>
      </div>
    )
  }
}

export default ModuleCards
