import React, {Component, PropTypes} from 'react'
import {Link} from 'react-router'

import withWidth from 'material-ui/utils/withWidth'
import CircularProgress from 'material-ui/CircularProgress'
import Dialog from 'material-ui/Dialog'
import FlatButton from 'material-ui/FlatButton'
import MenuItem from 'material-ui/MenuItem'
import RaisedButton from 'material-ui/RaisedButton'
import RefreshIndicator from 'material-ui/RefreshIndicator'
import SelectField from 'material-ui/SelectField'
import {Table, TableBody, TableRow, TableRowColumn} from 'material-ui/Table'
import TextField from 'material-ui/TextField'

import CCAPI from '../api'


/**
 * /schemas/newページのレンダリング
 * Schemaを作成する
 */
class SchemaCreatePage extends Component {
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
      isPosting: false,
      isError: false,
      response: {
        propertyTypeList: [],
      },
      value: {
        display_name: '',
        properties: [{
          name: '',
          type: '',
        }],
        metadata: {
          memo: '',
        },
      },
    }
  }

  /**
   * @override
   */
  async componentDidMount() {
    this.setState({isLoading: true})

    let response = await CCAPI.getSchemaPropertyTypes()
    let propertyTypeList = response.property_types

    this.setState({
      isLoading: false,
      response: {
        ...this.state.response,
        propertyTypeList: propertyTypeList,
      },
    })
  }

  /**
   * Createクリック Schemaを作成する
   */
  async handleClickCreate() {
    this.setState({isPosting: true})
    let response = await CCAPI.postSchema(this.state.value)

    this.setState({isPosting: false})
    switch (response.result) {
    case 'success':
      this.context.router.replace('/schemas/')
      break
    case 'failure':
    default:
      this.setState({isError: true})
    }
  }

  /**
   * @override
   */
  render() {
    let {isLoading, isPosting, isError, response, value} = this.state

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

    if(isPosting) {
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
        <Table selectable={false}>
          <TableBody displayRowCheckbox={false}>
            <TableRow>
              <TableRowColumn>名前</TableRowColumn>
              <TableRowColumn>
                <TextField
                  name="display_name"
                  hintText="Option"
                  fullWidth={true}
                  value={value.display_name}
                  onChange={ (e) =>
                    this.setState({value: {
                      ...value,
                      display_name: e.target.value,
                    }})
                  }
                />
              </TableRowColumn>
            </TableRow>
            <TableRow>
              <TableRowColumn>プロパティ</TableRowColumn>
              <TableRowColumn>
                <Table selectable={false}>
                  <TableBody displayRowCheckbox={false}>
                    {value.properties.map((property, index) => {
                      return (
                        <TableRow key={index}>
                          <TableRowColumn>
                            <TextField
                              name="proparty-name"
                              floatingLabelText="name"
                              value={property.name}
                              onChange={ (e) => {
                                let properties = value.properties
                                properties[index].name = e.target.value
                                this.setState({value: {
                                  ...value,
                                  properties: properties,
                                }})
                              }}
                            />
                          </TableRowColumn>
                          <TableRowColumn>
                            <SelectField
                              floatingLabelText="type"
                              value={property.type}
                              onChange={ (e, i, val) => {
                                let properties = value.properties
                                properties[index].type = val
                                this.setState({value: {
                                  ...value,
                                  properties: properties,
                                }})
                              }}
                            >
                              {response.propertyTypeList.map((propertyType) =>
                                <MenuItem
                                  key={propertyType}
                                  value={propertyType}
                                  primaryText={propertyType}
                                />)
                              }
                            </SelectField>
                          </TableRowColumn>
                          <TableRowColumn>
                            <RaisedButton
                              label="Remove"
                              secondary={true}
                              disabled={value.properties.length === 1 ? true : false}
                              onClick={ () => {
                                let properties = value.properties.filter((prop, i) => {
                                  return i !== index
                                })
                                this.setState({value: {
                                  ...value,
                                  properties: properties,
                                }})
                              }}
                            />
                          </TableRowColumn>
                        </TableRow>
                      )
                    })}
                    <TableRow>
                      <TableRowColumn colSpan="3">
                        <RaisedButton
                          label="Add New Property"
                          primary={true}
                          onClick={ () => {
                            this.setState({value: {
                              ...value,
                              properties: [
                                ...value.properties,
                                {
                                  name: '',
                                  type: '',
                                },
                              ],
                            }})
                          }}
                        />
                      </TableRowColumn>
                    </TableRow>
                  </TableBody>
                </Table>
              </TableRowColumn>
            </TableRow>
            <TableRow>
              <TableRowColumn>メタデータ</TableRowColumn>
              <TableRowColumn>
                <TextField
                  name="memo"
                  floatingLabelText="memo"
                  hintText="Option"
                  fullWidth={true}
                  multiLine={true}
                  rows={4}
                  rowsMax={4}
                  onChange={ (e) =>
                    this.setState({value: {
                      ...value,
                      metadata: {
                        ...value.metadata,
                        memo: e.target.value,
                      },
                    }})
                  }
                />
              </TableRowColumn>
            </TableRow>
          </TableBody>
        </Table>
        <Link to="/schemas/">
          <RaisedButton
            label="Cancel"
            secondary={true}
          />
        </Link>
        <RaisedButton
          label="Create"
          primary={true}
          disabled={
            (value.properties.length === 1
              && (value.properties[0].name.length === 0 || value.properties[0].type.length === 0))
            || (value.properties.filter( (property) => {
              return property.name.length === 0 ^ property.type.length === 0
            }).length !== 0) ? true : false}
          onClick={::this.handleClickCreate}
        />
        <Dialog
          title="Error"
          actions={[
            <FlatButton
              label="Close"
              onClick={ () => this.setState({isError: false})}
            />,
          ]}
          modal={true}
          open={isError}
        >
          Error!
        </Dialog>
      </div>
    )
  }
}

export default withWidth()(SchemaCreatePage)
