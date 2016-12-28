import React, {Component, PropTypes} from 'react'
import {Link} from 'react-router'

import withWidth from 'material-ui/utils/withWidth'
import {blueGrey600} from 'material-ui/styles/colors'
import Dialog from 'material-ui/Dialog'
import FlatButton from 'material-ui/FlatButton'
import RaisedButton from 'material-ui/RaisedButton'
import RefreshIndicator from 'material-ui/RefreshIndicator'
import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn} from 'material-ui/Table'

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
      deleteAsked: false,
      isDeleting: false,
      isError: false,
      deletingSchema: null,
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
   * Delete(Dialog)クリック Schemaを削除する
   */
  async handleClickDelete() {
    let schemaId = this.state.deletingSchema.uuid
    this.setState({
      deleteAsked: false,
      deletingSchema: null,
      isDeleting: true,
    })
    let response = await CCAPI.deleteSchema(schemaId)

    this.setState({
      isDeleting: false,
    })
    switch (response.result) {
    case 'success': {
      this.setState({isLoading: true})
      let response = await CCAPI.getSchemas()
      let schemaList = response.schemas

      this.setState({
        isLoading: false,
        schemaList: schemaList,
      })
      break
    }
    case 'failure':
    default:
      this.setState({isError: true})
    }
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

    if(this.state.isLoading) {
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

    if(this.state.isDeleting) {
      return (
        <div>
          <CircularProgress
            size={50}
            left={70}
            top={0}
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

            {this.state.schemaList.map((schema) => {
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
                    <RaisedButton
                      label="Delete"
                      secondary={true}
                      disabled={schema.modules.length === 0 ? false : true}
                      onClick={ () => this.setState({
                        deleteAsked: true,
                        deletingSchema: schema,
                      })}
                    />
                  </TableRowColumn>
                </TableRow>
              )
            })}

          </TableBody>

        </Table>
        <Dialog
          title="Delete Schema?"
          actions={[
            <FlatButton
              label="Cancel"
              onClick={ () => this.setState({
                deleteAsked: false,
                deletingSchema: null,
              })}
            />,
            <FlatButton
              label="Delete"
              onClick={::this.handleClickDelete}
            />,
          ]}
          modal={true}
          open={this.state.deleteAsked}
        >
          {(() => {
            let s = this.state.deletingSchema
            if (s !== null)
              return (
                <div>
                  <p>{s.display_name}</p>
                  <p>{s.uuid}</p>
                </div>
              )
            return ''
          })()}
        </Dialog>
        <Dialog
          title="Error"
          actions={[
            <FlatButton
              label="Close"
              onClick={ () => this.setState({isError: false})}
            />,
          ]}
          modal={true}
          open={this.state.isError}
        >
          Error!
        </Dialog>
      </div>
    )
  }
}

export default withWidth()(SchemaListPage)
