import React, {Component, PropTypes} from 'react'


/**
 */
class MemoArea extends Component {
  static propTypes = {
    schema: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      schema,
    } = this.props

    return (
      <div>
        {schema.memo}
      </div>
    )
  }
}

export default MemoArea
