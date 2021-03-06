import PropTypes from 'prop-types'
import React from 'react'

import Paper from 'material-ui/Paper'
import {blue500} from 'material-ui/styles/colors'

import IdLabel from 'src/components/commons/IdLabel'
import UrlLabel from 'src/components/commons/UrlLabel'


/**
 * 表示名エリア
 */
class DisplayNamePaper extends React.Component {
  static propTypes = {
    obj: PropTypes.object.isRequired,
    secondaryType: PropTypes.string,
  }

  /**
   * @override
   */
  render() {
    const {
      obj,
      secondaryType = 'id',
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

    const SecondaryLabel =
      secondaryType === 'id' ? IdLabel :
        secondaryType === 'url' ? UrlLabel :
          () => null

    return (
      <Paper>
        <div style={style.root}>
          <div style={style.displayName}>
            {obj.displayName || '(no name)'}
          </div>
          <SecondaryLabel
            obj={obj}
          />
        </div>
      </Paper>
    )
  }
}

export default DisplayNamePaper
