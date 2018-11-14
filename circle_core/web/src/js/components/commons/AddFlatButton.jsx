import React, {Component, PropTypes} from 'react'

import CCFlatButton from 'src/components/bases/CCFlatButton'
import {AddIcon} from 'src/components/bases/icons'


/**
 * 追加フラットボタン
 */
class AddFlatButton extends Component {
  static propTypes = {
    label: PropTypes.string,
  }

  /**
   * @override
   */
  render() {
    const {
      label = '追加する',
      ...other
    } = this.props

    return (
      <CCFlatButton
        label={label}
        icon={AddIcon}
        primary={true}
        {...other}
      />
    )
  }
}

export default AddFlatButton
