import React, {Component, PropTypes} from 'react'

import Tooltip from 'material-ui/internal/Tooltip'
import {grey900} from 'material-ui/styles/colors'


/**
 */
class DisplayNameLabel extends Component {
  static propTypes = {
    schema: PropTypes.object.isRequired,
  }

  state = {
    hovered: false,
  }

  /**
   * @override
   */
  render() {
    const {
      schema,
    } = this.props

    const style = {
      root: {
        position: 'relative',
        fontSize: 14,
        fontWeight: 'bold',
        color: grey900,
      },
    }

    return (
      <div
        style={style.root}
        onMouseEnter={() => this.setState({hovered: true})}
        onMouseLeave={() => this.setState({hovered: false})}
      >
        {schema.displayName || '(no name)'}
        <Tooltip
          label={schema.uuid}
          show={this.state.hovered}
        />
      </div>
    )
  }
}

export default DisplayNameLabel
