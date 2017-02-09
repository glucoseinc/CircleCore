import React, {Component, PropTypes} from 'react'

import Paper from 'material-ui/Paper'
import {blue500} from 'material-ui/styles/colors'

import IdLabel from 'src/components/commons/IdLabel'
import UrlLabel from 'src/components/commons/UrlLabel'


/**
 * 表示名エリア
 */
class DisplayNamePaper extends Component {
  static propTypes = {
    obj: PropTypes.object.isRequired,
    secondayType: PropTypes.string,
    onCopyButtonTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      obj,
      secondayType = 'id',
      onCopyButtonTouchTap,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
        padding: 24,
      },
      displayName: {
        fontSize: 20,
        fontWeight: 'bold',
        color: blue500,
      },
    }

    const SecondaryLabel = secondayType === 'id' ? IdLabel : UrlLabel

    return (
      <Paper>
        <div style={style.root}>
          <div style={style.displayName}>
            {obj.displayName || '(no name)'}
          </div>
          <SecondaryLabel
            obj={obj}
            onCopyButtonTouchTap={onCopyButtonTouchTap}
          />
        </div>
      </Paper>
    )
  }
}

export default DisplayNamePaper
