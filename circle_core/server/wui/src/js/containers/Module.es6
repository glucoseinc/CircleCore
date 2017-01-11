import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'

import {Card, CardActions, CardHeader, CardMedia} from 'material-ui/Card'
import {GridList, GridTile} from 'material-ui/GridList'
import RaisedButton from 'material-ui/RaisedButton'
import Subheader from 'material-ui/Subheader'
import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn} from 'material-ui/Table'

import * as actions from '../actions/module'
import Fetching from '../components/Fetching'
import ModuleInfo from '../components/ModuleInfo'


/**
 */
class Module extends Component {
  static propTypes = {
    isFetching: PropTypes.bool.isRequired,
    isDeleteAsking: PropTypes.bool.isRequired,
    modules: PropTypes.array.isRequired,
    params: PropTypes.object.isRequired,
    actions: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  render() {
    const {
      isFetching,
      modules,
      params,
      actions,
    } = this.props

    if (isFetching) {
      return (
        <Fetching />
      )
    }

    const module = modules.filter((_module) => _module.uuid === params.moduleId)[0]

    if (module === undefined) {
      return (
        <div>
          {params.moduleId}は存在しません
        </div>
      )
    }

    return (
      <div>
        <RaisedButton
          label="Create Shared Link"
          primary={true}
          onTouchTap={actions.createLinkTouchTap}
        />
        <GridList
          cellHeight="auto"
        >
          <GridTile cols={2}>
            <ModuleInfo module={module} />
          </GridTile>
          {module.messageBoxes.map((messageBox) =>
            <GridTile key={messageBox.uuid}>
              <Card style={{margin: 4}}>
                <CardHeader
                  title={messageBox.displayName}
                />
                <CardMedia style={{paddingLeft: 16, paddingRight: 16}}>
                  <Card>
                    <CardMedia style={{paddingLeft: 16, paddingRight: 16}}>
                      <div>
                        Graph
                      </div>
                    </CardMedia>
                  </Card>
                  <Card>
                    <CardHeader
                      title="Message schema"
                      subtitle={messageBox.schema.displayName}
                    />
                    <CardMedia style={{paddingLeft: 16, paddingRight: 16}}>
                      <div>
                        <Table selectable={false}>
                          <TableHeader displaySelectAll={false} adjustForCheckbox={false}>
                            <TableRow>
                              <TableHeaderColumn>Name</TableHeaderColumn>
                              <TableHeaderColumn>Type</TableHeaderColumn>
                            </TableRow>
                          </TableHeader>

                          <TableBody displayRowCheckbox={false}>
                            {messageBox.schema.properties.map((property, index) => {
                              return (
                                <TableRow key={index}>
                                  <TableRowColumn>{property.name}</TableRowColumn>
                                  <TableRowColumn>{property.type}</TableRowColumn>
                                </TableRow>
                              )
                            })}
                          </TableBody>
                        </Table>
                      </div>
                      <div>
                        <Subheader>Memo</Subheader>
                        <div style={{paddingLeft: 16}}>
                          {messageBox.schema.metadata.memo}
                        </div>
                      </div>
                    </CardMedia>
                  </Card>
                </CardMedia>
                <CardActions>
                  <RaisedButton
                    label="Edit"
                  />
                  <RaisedButton
                    label="Download"
                  />
                  <RaisedButton
                    label="Delete"
                    secondary={true}
                  />
                </CardActions>
              </Card>
            </GridTile>
          )}
        </GridList>
        <RaisedButton
          label="Delete this module"
          secondary={true}
          onTouchTap={actions.deleteTouchTap}
        />
      </div>
    )
  }
}


/**
 * [mapStateToProps description]
 * @param  {[type]} state [description]
 * @return {[type]}       [description]
 */
function mapStateToProps(state) {
  return {
    isFetching: state.asyncs.isModulesFetching,
    isDeleteAsking: state.asyncs.isModuleDeleteAsking,
    modules: state.entities.modules,
  }
}

/**
 * [mapDispatchToProps description]
 * @param  {[type]} dispatch [description]
 * @return {[type]}          [description]
 */
function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(actions, dispatch),
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Module)
