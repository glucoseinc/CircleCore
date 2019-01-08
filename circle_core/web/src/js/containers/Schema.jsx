import {routerActions} from 'connected-react-router'
import PropTypes from 'prop-types'
import React from 'react'
import {connect} from 'react-redux'

import actions from 'src/actions'
import {urls} from 'src/routes'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'

import SchemaDeleteDialog from 'src/components/commons/SchemaDeleteDialog'

import SchemaDetail from 'src/components/SchemaDetail'


/**
 * Schema詳細
 */
class Schema extends React.Component {
  static propTypes = {
    isSchemaFetching: PropTypes.bool.isRequired,
    isCcInfoFetching: PropTypes.bool.isRequired,
    schemas: PropTypes.object.isRequired,
    ccInfos: PropTypes.object.isRequired,
    params: PropTypes.object.isRequired,
    setTitle: PropTypes.func,
    onBackButtonClick: PropTypes.func,
    onDeleteOkButtonClick: PropTypes.func,
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
  onDeleteClick() {
    this.setState({
      isSchemaDeleteDialogOpen: true,
    })
  }

  /**
   * 削除ダイアログのボタン押下時の動作
   * @param {bool} execute
   * @param {object} schema
   */
  onDeleteDialogButtonClick(execute, schema) {
    this.setState({
      isSchemaDeleteDialogOpen: false,
    })
    if (execute && schema) {
      this.props.onDeleteOkButtonClick(schema)
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
      isSchemaFetching,
      isCcInfoFetching,
      schemas,
      ccInfos,
      params,
      onBackButtonClick,
    } = this.props

    if (isSchemaFetching || isCcInfoFetching) {
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

    const ownCcInfo = ccInfos.filter((ccInfo) => ccInfo.myself).first()

    return (
      <div className="page">
        <SchemaDetail
          schema={schema}
          ownCcInfo={ownCcInfo}
          onBackClick={onBackButtonClick}
          onDeleteClick={::this.onDeleteClick}
        />

        <SchemaDeleteDialog
          open={isSchemaDeleteDialogOpen}
          schema={schema}
          onOkClick={(schema) => this.onDeleteDialogButtonClick(true, schema)}
          onCancelClick={() => this.onDeleteDialogButtonClick(false)}
        />
      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  isSchemaFetching: state.asyncs.isSchemaFetching,
  isCcInfoFetching: state.asyncs.isCcInfoFetching,
  schemas: state.entities.schemas,
  ccInfos: state.entities.ccInfos,
})

const mapDispatchToProps = (dispatch) => ({
  setTitle: (title) => dispatch(actions.page.setTitle(title)),
  onBackButtonClick: () => dispatch(routerActions.push(urls.schemas.fullPath)),
  onDeleteOkButtonClick: (schema) => dispatch(actions.schema.deleteRequest(schema.uuid)),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Schema)
