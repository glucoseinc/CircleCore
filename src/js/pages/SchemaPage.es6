import React, {Component, PropTypes} from 'react'

import withWidth from 'material-ui/utils/withWidth'
import RefreshIndicator from 'material-ui/RefreshIndicator'
import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn} from 'material-ui/Table'

import CCAPI from '../api'

/**
 * /schemas/:schemaIdページのレンダリング
 * Schemaの詳細を表示する
 */
class SchemaPage extends Component {
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
      schema: null,
    }
  }

  /**
   * @override
   */
  async componentDidMount() {
    this.setState({isLoading: true})

    let response = await CCAPI.getSchema(this.props.params.schemaId)
    let schema = response.schema

    this.setState({
      isLoading: false,
      schema: schema,
    })
  }

  /**
   * @override
   */
  render() {
    let {isLoading, schema} = this.state

    if (isLoading) {
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
        <Table selectable={false}>
          <TableBody displayRowCheckbox={false}>
            <TableRow>
              <TableRowColumn>名前</TableRowColumn>
              <TableRowColumn>{schema.display_name}</TableRowColumn>
            </TableRow>
            <TableRow>
              <TableRowColumn>UUID</TableRowColumn>
              <TableRowColumn>{schema.uuid}</TableRowColumn>
            </TableRow>
            <TableRow>
              <TableRowColumn>プロパティ</TableRowColumn>
              <TableRowColumn>
                <Table selectable={false}>
                  <TableHeader displaySelectAll={false} adjustForCheckbox={false}>
                    <TableRow>
                      <TableHeaderColumn>Name</TableHeaderColumn>
                      <TableHeaderColumn>Type</TableHeaderColumn>
                    </TableRow>
                  </TableHeader>

                  <TableBody displayRowCheckbox={false}>
                    {schema.properties.map((property) => {
                      return (
                        <TableRow>
                          <TableRowColumn>{property.name}</TableRowColumn>
                          <TableRowColumn>{property.type}</TableRowColumn>
                        </TableRow>
                      )
                    })}
                  </TableBody>
                </Table>
              </TableRowColumn>
            </TableRow>
            <TableRow>
              <TableRowColumn>メタデータ</TableRowColumn>
              <TableRowColumn>
                <p>メモ</p>
                <p>{schema.metadata.memo}</p>
              </TableRowColumn>
            </TableRow>
          </TableBody>
        </Table>
      </div>
    )
  }
}

export default withWidth()(SchemaPage)
