import React, {Component, PropTypes} from 'react'
import {Link} from 'react-router'
import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn} from 'material-ui/Table'
import RefreshIndicator from 'material-ui/RefreshIndicator'
import withWidth from 'material-ui/utils/withWidth'
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
      isLoading: true,
      moduleList: [],
    }
  }

  /**
   * @override
   */
  async componentDidMount() {
    // TODO: moduleListを取りに行く
    this.setState({isLoading: true})
    let response = await CCAPI.listModules()
    let moduleList = response.modules

    this.setState({isLoading: false, moduleList})
  }
  /**
   * @override
   */
  render() {
    const styles = {
      subtext: {
        color: blueGrey600,
        fontSize: 10,
      },
    }
    let {muiTheme} = this.context
    let {isLoading, moduleList} = this.state

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
                    <Link to={`/modules/${module.uuid}`}>
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
