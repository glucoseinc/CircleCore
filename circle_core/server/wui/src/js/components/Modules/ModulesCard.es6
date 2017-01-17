import React, {Component, PropTypes} from 'react'

import FlatButton from 'material-ui/FlatButton'
import {GridList, GridTile} from 'material-ui/GridList'
import Paper from 'material-ui/Paper'

import CCLink from '../../components/CCLink'
import {urls} from '../../routes'


/**
 */
class ModulesCard extends Component {
  static propTypes = {
    timeAxisUnit: PropTypes.number,
    modules: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      modules,
      timeAxisUnit = 0,
    } = this.props

    const dummyGraph = '/static/images/dummy_graph.png'

    return (
      <div>
        <Paper>
          <FlatButton label="30分" primary={timeAxisUnit==0} />
          <FlatButton label="1時間" primary={timeAxisUnit==1} />
          <FlatButton label="6時間" primary={timeAxisUnit==2} />
          <FlatButton label="1日" primary={timeAxisUnit==3} />
          <FlatButton label="7日" primary={timeAxisUnit==4} />
        </Paper>
        <GridList
          cellHeight="auto"
        >
          {modules.valueSeq().map((module) => {
            return (
              <GridTile
                key={module.uuid}
              >
                <CCLink
                  url={urls.module}
                  params={{moduleId: module.uuid}}
                >
                  <Paper>
                  {module.label} <br />
                  <img src={dummyGraph} width="100%" height="100%"/>
                  </Paper>
                </CCLink>
              </GridTile>
            )
          })}
        </GridList>
      </div>
    )
  }
}


export default ModulesCard
