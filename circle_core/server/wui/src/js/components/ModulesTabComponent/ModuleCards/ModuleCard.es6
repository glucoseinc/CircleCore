import React, {Component, PropTypes} from 'react'

import {Card, CardMedia, CardTitle} from 'material-ui/Card'

import {colorUUID} from 'src/colors'
import {urls} from 'src/routes'

import CCLink from 'src/components/commons/CCLink'

import ModuleGraph from 'src/components/commons/ModuleGraph'


/**
 * ModuleCard
 */
class ModuleCard extends Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    autoUpdate: PropTypes.bool.isRequired,
    graphRange: PropTypes.string.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      module,
      autoUpdate,
      graphRange,
    } = this.props

    return (
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
    )
  }
}

export default ModuleCard
