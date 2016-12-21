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
class ModuleListPage extends Component {
  static propTypes = {
    width: PropTypes.number.isRequired,
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
      isLoading: false,
      moduleList: [
        {display_name: 'test', uuid: '0C92D140-6E74-4F6D-B2FA-4CC124DBC6DC'},
      ]
    }
  }

  /**
   * @override
   */
  async componentDidMount() {
    // TODO: moduleListを取りに行く
    this.setState({loading: true})

    let moduleList = await CCAPI.listModules()

    this.setState({loading: false, moduleList})
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
    let {muiTheme} = this.context
    let {isLoading, moduleList} = this.state

    return (
      <div>
        <Table>

          <TableHeader
            displaySelectAll={false}
            adjustForCheckbox={false}
          >
            <TableRow>
              <TableHeaderColumn tooltip="Module's name">Name</TableHeaderColumn>
            </TableRow>
          </TableHeader>

          <TableBody
            displayRowCheckbox={false}
          >

            {moduleList.map((module) => {
              return (
                <TableRow key={module.uuid}>
                  <TableRowColumn>
                    <Link to={`/module/${module.uuid}`}>
                      {module.display_name}<br />
                      <span style={muiTheme.prepareStyles(styles.subtext)}>{module.uuid}</span>
                    </Link>
                  </TableRowColumn>
                  <TableRowColumn>
                    MessageBox
                  </TableRowColumn>
                  <TableRowColumn>
                    Tag
                  </TableRowColumn>
                </TableRow>
              )
            })}

          </TableBody>

        </Table>
      </div>
    )
  }
}

export default withWidth()(ModuleListPage)
