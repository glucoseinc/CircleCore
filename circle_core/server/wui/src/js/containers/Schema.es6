import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'
import {routerActions} from 'react-router-redux'

import actions from 'src/actions'
import {urls} from 'src/routes'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'

import SchemaDeleteDialog from 'src/components/commons/SchemaDeleteDialog'

import SchemaDetail from 'src/components/SchemaDetail'


/**
 * Schema詳細
 */
class Schema extends Component {
  static propTypes = {
    isFetching: PropTypes.bool.isRequired,
    schemas: PropTypes.object.isRequired,
    params: PropTypes.object.isRequired,
    setTitle: PropTypes.func,
    onBackButtonTouchTap: PropTypes.func,
    onDeleteOkButtonTouchTap: PropTypes.func,
  }

  state = {
    isSchemaDeleteDialogOpen: false,
  }

  /**
   * @override
   */
  componentWillReceiveProps(nextProps) {
    const schema = nextProps.schemas.get(nextProps.params.schemaId)
    const title = schema !== undefined ? schema.label : ''
    this.props.setTitle(title)
  }

  /**
   * 削除ボタン押下時の動作
   */
  onDeleteTouchTap() {
    this.setState({
      isSchemaDeleteDialogOpen: true,
    })
  }

  /**
   * 削除ダイアログのボタン押下時の動作
   * @param {bool} execute
   * @param {object} schema
   */
  onDeleteDialogButtonTouchTap(execute, schema) {
    this.setState({
      isSchemaDeleteDialogOpen: false,
    })
    if (execute && schema) {
      this.props.onDeleteOkButtonTouchTap(schema)
    }
  }

  /**
   * @override
   */
  render() {
    const {
      isSchemaDeleteDialogOpen,
    } = this.state
    const {
      isFetching,
      schemas,
      params,
      onBackButtonTouchTap,
    } = this.props

    if (isFetching) {
      return (
        <LoadingIndicator />
      )
    }

    const schema = schemas.get(params.schemaId)

    if (schema === undefined) {
      return (
        <div>
          {params.schemaId}は存在しません
        </div>
      )
    }

    return (
      <div className="page">
        <SchemaDetail
          schema={schema}
          onBackTouchTap={onBackButtonTouchTap}
          onDeleteTouchTap={::this.onDeleteTouchTap}
        />

        <SchemaDeleteDialog
          open={isSchemaDeleteDialogOpen}
          schema={schema}
          onOkTouchTap={(schema) => this.onDeleteDialogButtonTouchTap(true, schema)}
          onCancelTouchTap={() => this.onDeleteDialogButtonTouchTap(false)}
        />
      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  isFetching: state.asyncs.isSchemaFetching,
  schemas: state.entities.schemas,
})

const mapDispatchToProps = (dispatch) => ({
  setTitle: (title) => dispatch(actions.page.setTitle(title)),
  onBackButtonTouchTap: () => dispatch(routerActions.push(urls.schemas.fullPath)),
  onDeleteOkButtonTouchTap: (schema) => dispatch(actions.schemas.deleteRequest(schema.uuid)),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Schema)
