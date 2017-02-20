import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'
import {routerActions} from 'react-router-redux'

import AppBar from 'material-ui/AppBar'
import Snackbar from 'material-ui/Snackbar'
import Title from 'react-title-component'

import actions from 'src/actions'
import ErrorDialog from 'src/components/ErrorDialog'


/**
 * フレーム
 * src/containers/Masterのサブセット
 */
class PublicFrame extends Component {
  static propTypes = {
    title: PropTypes.string,
    isSnackbarOpen: PropTypes.bool,
    snackbarMessage: PropTypes.string,
    isErrorDialogOpen: PropTypes.bool,
    errorDialogMessages: PropTypes.object,
    location: PropTypes.object.isRequired,
    children: PropTypes.node.isRequired,
    onLocationChange: PropTypes.func,
    onSnackBarCloseRequest: PropTypes.func,
    onErrorDialogCloseRequest: PropTypes.func,
  }

  /**
   *@override
   */
  render() {
    const {
      title = '',
      isSnackbarOpen = false,
      snackbarMessage = '',
      onSnackBarCloseRequest,
      isErrorDialogOpen = false,
      onErrorDialogCloseRequest,
      errorDialogMessages = {},
      children,
    } = this.props

    const style = {
      content: {
      },
      children: {
      },
    }

    return (
      <div>
        <Title render="CircleCore" />
        <div style={style.content}>
          <AppBar
            title={title}
            showMenuIconButton={false}
          />
          <div style={style.children}>
            {children}
          </div>
        </div>

        <Snackbar
          open={isSnackbarOpen}
          message={snackbarMessage}
          autoHideDuration={4000}
          onRequestClose={onSnackBarCloseRequest}
        />

        <ErrorDialog
          open={isErrorDialogOpen}
          messages={errorDialogMessages}
          onCloseRequest={onErrorDialogCloseRequest}
        />

      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  title: state.page.title,
  isSnackbarOpen: state.page.isSnackbarOpen,
  snackbarMessage: state.page.snackbarMessage,
  isErrorDialogOpen: state.page.isErrorDialogOpen,
  errorDialogMessages: state.page.errorDialogMessages,
})

const mapDispatchToProps = (dispatch)=> ({
  onLocationChange: (pathname) => dispatch(routerActions.push(pathname)),
  onSnackBarCloseRequest: () => dispatch(actions.page.hideSnackbar()),
  onErrorDialogCloseRequest: () => dispatch(actions.page.hideErrorDialog()),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(PublicFrame)
