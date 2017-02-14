import React, {Component, PropTypes} from 'react'

import Paper from 'material-ui/Paper'
import {grey400, grey700} from 'material-ui/styles/colors'

/**
* Empty
*/
class Empty extends Component {
  static propTypes = {
    icon: PropTypes.func.isRequired,
    itemName: PropTypes.string,
    primaryLabel: PropTypes.string,
    secondaryLabel: PropTypes.string,
  }

  /**
   * @override
   */
  render() {
    const {
      icon,
      itemName,
      primaryLabel,
      secondaryLabel,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'column nowrap',
        alignItems: 'center',
      },

      iconArea: {
        paddingTop: 200,
      },
      paper: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        width: 148,
        height: 148,
      },
      icon: {
        width: 100,
        height: 100,
      },

      primaryLabel: {
        paddingTop: 72,
        fontSize: 24,
        lineHeight: 1,
        color: grey700,
      },
      secondaryLabel: {
        paddingTop: 16,
        fontSize: 14,
        lineHeight: 1,
        color: grey700,
      },
    }

    const Icon = icon

    const generatedPrimaryLabel = primaryLabel
      || (itemName && `${itemName}のアイテムがありません。`)
      || 'アイテムがありません。'

    const generatedSecondaryLabel = secondaryLabel
      || (itemName && `新しく追加するとここに${itemName}が表示されます。`)
      || '新しく追加するとここにアイテムが表示されます。'

    return (
      <div style={style.root}>
        <div style={style.iconArea}>
          <Paper style={style.paper} circle={true}>
            <Icon style={style.icon} color={grey400}/>
          </Paper>
        </div>
        <div style={style.primaryLabel}>{generatedPrimaryLabel}</div>
        <div style={style.secondaryLabel}>{generatedSecondaryLabel}</div>
      </div>
    )
  }
}

export default Empty
