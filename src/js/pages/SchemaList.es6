import React, {Component, PropTypes} from 'react'
import {Link} from 'react-router'
import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn} from 'material-ui/Table'
import {FlatButton, RaisedButton} from 'material-ui'
import RefreshIndicator from 'material-ui/RefreshIndicator'
import withWidth from 'material-ui/utils/withWidth'
import {blueGrey600} from 'material-ui/styles/colors'

import CCAPI from '../api'


/**
 * /schemas/ページのレンダリング
 * Schemaのリストを表示する
 */
class SchemaListPage extends Component {
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
      schemaList: [],
    }
  }

  /**
   * @override
   */
  async componentDidMount() {
    this.setState({isLoading: true})
    let response = await CCAPI.getSchemas()
    let schemaList = response.schemas

    this.setState({
      isLoading: false,
      schemaList: schemaList,
    })
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
    let {isLoading, schemaList} = this.state

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
        <Link to="/schemas/new">
          <RaisedButton label="Add" primary={true} />
        </Link>
        <Table>

          <TableHeader
            displaySelectAll={false}
            adjustForCheckbox={false}
          >
            <TableRow>
              <TableHeaderColumn tooltip="Schema's name">Name</TableHeaderColumn>
              <TableHeaderColumn tooltip="Modules using schema">Modules</TableHeaderColumn>
              <TableHeaderColumn></TableHeaderColumn>
            </TableRow>
          </TableHeader>

          <TableBody
            displayRowCheckbox={false}
          >

            {schemaList.map((schema) => {
              return (
                <TableRow key={schema.uuid}>
                  <TableRowColumn>
                    <Link to={`/schemas/${schema.uuid}`}>
                      {schema.display_name}<br/>
                      <span style={styles.subtext}>{schema.uuid}</span>
                    </Link>
                  </TableRowColumn>
                  <TableRowColumn>
                    {schema.modules.map((module) =>
                      <Link key={module.uuid} to={`/modules/${module.uuid}`}>
                        <FlatButton key={module.uuid} label={module.display_name ? module.display_name : module.uuid}/>
                      </Link>
                    )}
                  </TableRowColumn>
                  <TableRowColumn>
                    <Link to={`/schemas/${schema.uuid}/delete`}>
                      <RaisedButton label="Delete" secondary={true} />
                    </Link>
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

export default withWidth()(SchemaListPage)
