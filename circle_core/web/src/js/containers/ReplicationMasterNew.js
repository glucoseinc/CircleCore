import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'
import Paper from 'material-ui/Paper'
import TextField from 'material-ui/TextField'

import actions from 'src/actions'
import ReplicationMaster from 'src/models/ReplicationMaster'
import CreateButton from 'src/components/commons/CreateButton'


/**
 * Module作成
 */
class ReplicationMasterNew extends Component {
  static propTypes = {
    onCreateTouchTap: PropTypes.func,
  }

  state = {
    replicationMaster: new ReplicationMaster(),
  }

  /**
   * @override
   */
  render() {
    const {
      replicationMaster,
    } = this.state

    const style = {
      root: {
        padding: 24,
      },
      actionsArea: {
        display: 'flex',
        flexFlow: 'row nowrap',
        justifyContent: 'space-around',
        paddingTop: 40,
      },
    }

    return (
      <div className="page">
        <Paper style={style.root}>

          <TextField
            floatingLabelText="共有リンクURL"
            fullWidth={true}
            onChange={(event, newValue) => {
              this.setState({replicationMaster: replicationMaster.updateEndpointUrl(newValue)})
            }}
          />

          <div style={style.actionsArea}>
            <CreateButton
              disabled={replicationMaster.isReadyToCreate() ? false : true}
              onTouchTap={() => this.props.onCreateTouchTap(replicationMaster)}
            />
          </div>
        </Paper>
      </div>
    )
  }
}


const mapStateToProps = (state) => ({
})

const mapDispatchToProps = (dispatch) => ({
  onCreateTouchTap: (replicationMaster) => dispatch(actions.replicationMaster.createRequest(replicationMaster.toJS())),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(ReplicationMasterNew)
