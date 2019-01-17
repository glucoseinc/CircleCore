import PropTypes from 'prop-types'
import React from 'react'
import {connect} from 'react-redux'
import Paper from 'material-ui/Paper'
import TextField from 'material-ui/TextField'

import actions from 'src/actions'
import ReplicationMaster, {VALID_URL_REX} from 'src/models/ReplicationMaster'
import CreateButton from 'src/components/commons/CreateButton'

/**
 * Module作成
 */
class ReplicationMasterNew extends React.Component {
  static propTypes = {
    onCreateClick: PropTypes.func,
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

    // check url
    let errorText = ''

    if (replicationMaster.endpointUrl && !replicationMaster.endpointUrl.match(VALID_URL_REX)) {
      errorText = 'URLが間違っています'
    }


    return (
      <div className="page">
        <Paper style={style.root}>

          <TextField
            floatingLabelText="共有リンクURL"
            fullWidth={true}
            errorText={errorText}
            onChange={(event, newValue) => {
              this.setState({replicationMaster: replicationMaster.updateEndpointUrl(newValue)})
            }}
          />

          <div style={style.actionsArea}>
            <CreateButton
              disabled={replicationMaster.isReadyToCreate() ? false : true}
              onClick={() => this.props.onCreateClick(replicationMaster)}
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
  onCreateClick: (replicationMaster) => dispatch(actions.replicationMaster.createRequest(replicationMaster.toJS())),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(ReplicationMasterNew)
