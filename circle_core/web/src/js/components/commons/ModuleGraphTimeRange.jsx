import PropTypes from 'prop-types'
import React from 'react'

import FlatButton from 'material-ui/FlatButton'
import {grey200, redA200} from 'material-ui/styles/colors'

import {RANGES, RANGE_LABELS} from 'src/components/commons/ModuleGraph'


/**
* ModuleGraphTimeRange
*/
class ModuleGraphTimeRange extends React.Component {
  static propTypes = {
    activeTimeRange: PropTypes.string.isRequired,
    style: PropTypes.object,
    onTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      activeTimeRange,
      style,
      onTouchTap,
    } = this.props

    const mergedStyle = {
      root: {
        display: 'flex',
        flexFlow: 'row nowrap',
        background: grey200,
        ...style,
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
    }

    return (
      <div style={mergedStyle.root}>
        {RANGES.map((range) => (
          <FlatButton
            key={range}
            style={activeTimeRange === range ? mergedStyle.activeTimeRange : mergedStyle.timeRange}
            label={RANGE_LABELS[range]}
            labelStyle={activeTimeRange === range ? mergedStyle.activeTimeRangeLabel : mergedStyle.timeRangeLabel}
            onTouchTap={() => onTouchTap(range)}
          />
        ))}
      </div>
    )
  }
}


export default ModuleGraphTimeRange
