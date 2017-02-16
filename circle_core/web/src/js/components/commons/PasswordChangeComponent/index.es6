import React, {Component, PropTypes} from 'react'

import PasswordAutoGenerateComponent from './PasswordAutoGenerateComponent'
import PasswordManualChangeComponent from './PasswordManualChangeComponent'


/**
* パスワード変更コンポーネント
*/
class PasswordChangeComponent extends Component {
  static propTypes = {
    errors: PropTypes.object,
    onUpdate: PropTypes.func,
  }

  state = {
    autoGenerate: false,
  }

  /**
   * @override
   */
  render() {
    const {
      autoGenerate,
    } = this.state
    const {
      errors = {},
      onUpdate,
    } = this.props

    const PasswordChangeComponent_ = autoGenerate ? PasswordAutoGenerateComponent : PasswordManualChangeComponent

    return (
      <PasswordChangeComponent_
        errors={errors}
        onUpdate={onUpdate}
        onToggleInputMethod={() => this.setState({autoGenerate: !autoGenerate})}
      />
    )
  }
}


export default PasswordChangeComponent
