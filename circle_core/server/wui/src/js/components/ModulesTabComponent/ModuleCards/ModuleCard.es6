import React, {Component, PropTypes} from 'react'

import Paper from 'material-ui/Paper'

import IdLabel from 'src/components/commons/IdLabel'

import ModuleGraph from 'src/components/commons/ModuleGraph'


/**
 * ModuleCard
 */
class ModuleCard extends Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    autoUpdate: PropTypes.bool.isRequired,
    graphRange: PropTypes.string.isRequired,
    onDisplayNameTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      module,
      autoUpdate,
      graphRange,
      onDisplayNameTouchTap,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
      },

      infomations: {
        padding: '16px 24px',
        display: 'flex',
        flexFlow: 'column nowrap',
      },
      displayName: {
        fontSize: 14,
        fontWeight: 'bold',
        cursor: 'pointer',
      },
      id: {
        paddingTop: 8,
      },
    }

    return (
      <Paper>
        <div style={style.root}>
          <ModuleGraph module={module} range={graphRange} autoUpdate={autoUpdate ? 60 : 0} />
          <div style={style.infomations}>
            <div style={style.displayName} onTouchTap={() => onDisplayNameTouchTap(module)}>
              {module.displayName}
            </div>
            <div style={style.id}>
              <IdLabel
                obj={module}
              />
            </div>
          </div>
        </div>
      </Paper>
    )
  }
}

export default ModuleCard
