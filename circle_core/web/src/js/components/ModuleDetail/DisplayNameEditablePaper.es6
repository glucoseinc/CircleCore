import React, {Component, PropTypes} from 'react'

import Paper from 'material-ui/Paper'
import {blue500} from 'material-ui/styles/colors'

import ComponentWithIconButton from 'src/components/bases/ComponentWithIconButton'
import {EditIcon} from 'src/components/bases/icons'

import IdLabel from 'src/components/commons/IdLabel'
import UrlLabel from 'src/components/commons/UrlLabel'


/**
 * 表示名エリア(編集可能)
 */
class DisplayNameEditablePaper extends Component {
  static propTypes = {
    obj: PropTypes.object.isRequired,
    editDisabled: PropTypes.bool,
    secondaryType: PropTypes.string,
    onEditTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      obj,
      editDisabled = false,
      secondaryType = 'id',
      onEditTouchTap,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'row nowrap',
        padding: 24,
      },

      contents: {
        display: 'flex',
        flexFlow: 'column nowrap',
      },
      displayName: {
        fontSize: 20,
        fontWeight: 'bold',
        color: blue500,
      },
    }

    const SecondaryLabel = secondaryType === 'id' ? IdLabel : UrlLabel

    return (
      <Paper>
        <div style={style.root}>
          <ComponentWithIconButton
            icon={EditIcon}
            iconButtonDisabled={editDisabled}
            onIconButtonTouchTap={onEditTouchTap}
          >
            <div style={style.contents}>
              <div style={style.displayName}>
                {obj.displayName || '(no name)'}
              </div>
              <SecondaryLabel
                obj={obj}
              />
            </div>
          </ComponentWithIconButton>
        </div>
      </Paper>
    )
  }
}

export default DisplayNameEditablePaper
