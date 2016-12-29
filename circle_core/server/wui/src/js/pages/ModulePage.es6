import React, {Component, PropTypes} from 'react'
import RefreshIndicator from 'material-ui/RefreshIndicator'
import withWidth from 'material-ui/utils/withWidth'

import CCAPI from '../api'


/**
 * /modules/ページのレンダリング
 * モジュールのリストを表示する
 */
class ModulePage extends Component {
  static propTypes = {
    width: PropTypes.number.isRequired,
    params: PropTypes.object.isRequired,
  }

  static contextTypes = {
    muiTheme: PropTypes.object.isRequired,
    router: PropTypes.object.isRequired,
  }

  /**
   * @constructor
   */
  constructor(...args) {
    super(...args)

    this.state = {
      isLoading: true,
      module: null,
    }
  }

  /**
   * @override
   */
  async componentDidMount() {
    // TODO: moduleListを取りに行く
    this.setState({isLoading: true})

    let module = await CCAPI.getModule(this.props.params.moduleId)

    this.setState({isLoading: false, module: module})
  }

  /**
   * @override
   */
  render() {
    let {isLoading, module} = this.state

    if(isLoading) {
      return (
        <div>
          <RefreshIndicator
            size={50}
            left={70}
            top={0}
            loadingColor="#FF9800"
            status="loading"
            style={{
              display: 'inline-block',
              position: 'relative',
            }}
          />
        </div>
      )
    }

    return (
      <div>
        module: {module}{this.props.params.moduleId}
      </div>
    )
  }
}

export default withWidth()(ModulePage)
