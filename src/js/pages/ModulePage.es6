import React, {Component, PropTypes} from 'react'
import {Link} from 'react-router'
import {Table, TableBody, TableFooter, TableHeader, TableHeaderColumn, TableRow, TableRowColumn}
  from 'material-ui/Table'
import withWidth from 'material-ui/utils/withWidth'
import spacing from 'material-ui/styles/spacing'
import {blueGrey600} from 'material-ui/styles/colors'

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

  constructor(...args) {
    super(...args)

    this.state = {
      isLoading: true,
      module: null
    }
  }

  /**
   * @override
   */
  async componentDidMount() {
    // TODO: moduleListを取りに行く
    this.setState({loading: true})

    let module = await CCAPI.getModule(this.props.params.moduleId)

    this.setState({loading: false, module: module})
  }

  /**
   * @override
   */
  render() {
    const styles = {
      subtext: {
        color: blueGrey600,
        fontSize: 10,
      }
    }
    const style = {
      paddingTop: spacing.desktopKeylineIncrement,
    }
    let {muiTheme} = this.context
    let {isLoading, module} = this.state

    return (
      <div>
        module: {this.props.params.moduleId}
      </div>
    )
  }
}

export default withWidth()(ModulePage)
