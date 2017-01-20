import React, {Component, PropTypes} from 'react'

import FlatButton from 'material-ui/FlatButton'
import {Card, CardHeader, CardMedia} from 'material-ui/Card'
import Paper from 'material-ui/Paper'

import CCLink from '../../components/CCLink'
import {urls} from '../../routes'
import {ModuleGraph, RANGES, RANGE_LABELS} from './ModuleGraph'

/**
 */
class ModulesCards extends Component {
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
      graphRange,
    } = this.state

    return (
      <div>
        <Paper>
          {RANGES.map((r) => (
            <FlatButton
              key={r}
              label={RANGE_LABELS[r]}
              primary={graphRange === r}
              onTouchTap={() => this.setState({graphRange: r})}
            />
          ))}
        </Paper>

        <div className={`moduleCards moduleCards-col${cols}`}>
          {modules.valueSeq().map((module) => (
            <Card
              key={module.uuid}
              className="moduleCard"
            >
              <CardHeader
                title={
                  <CCLink url={urls.module} params={{moduleId: module.uuid}}>
                    {module.displayName}
                  </CCLink>}
              />
              <CardMedia>
                <ModuleGraph module={module} range={graphRange} />
              </CardMedia>
            </Card>
          ))}
        </div>
      </div>
    )
  }
}

export default ModulesCards
