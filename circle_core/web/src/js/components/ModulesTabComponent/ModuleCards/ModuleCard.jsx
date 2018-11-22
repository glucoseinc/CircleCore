import PropTypes from 'prop-types'
import React from 'react'

import Paper from 'material-ui/Paper'

import ModuleGraph from 'src/components/commons/ModuleGraph'


/**
 * ModuleCard
 */
class ModuleCard extends React.Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    autoUpdate: PropTypes.bool.isRequired,
    graphRange: PropTypes.string.isRequired,
    onDisplayNameClick: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      module,
      autoUpdate,
      graphRange,
      onDisplayNameClick,
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
    }

    return (
      <Paper>
        <div style={style.root}>
          <ModuleGraph module={module} range={graphRange} autoUpdate={autoUpdate ? 60 : 0} />
          <div style={style.infomations}>
            <div style={style.displayName} onClick={() => onDisplayNameClick(module)}>
              {module.displayName}
            </div>
          </div>
        </div>
      </Paper>
    )
  }
}

export default ModuleCard
