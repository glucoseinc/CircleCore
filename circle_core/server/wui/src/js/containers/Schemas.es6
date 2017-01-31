import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'
import {routerActions} from 'react-router-redux'

import Snackbar from 'material-ui/Snackbar'

import actions from 'src/actions'
import {urls, createPathName} from 'src/routes'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'

import AddFloatingActionButton from 'src/components/commons/AddFloatingActionButton'
import CCLink from 'src/components/commons/CCLink'
import SchemaDeleteDialog from 'src/components/commons/SchemaDeleteDialog'

import SchemaInfoPaper from 'src/components/SchemaInfoPaper'


/**
 * Schema一覧
 */
class Schemas extends Component {
  static propTypes = {
    isFetching: PropTypes.bool.isRequired,
    schemas: PropTypes.object.isRequired,
    modules: PropTypes.object.isRequired,
    onSchemaInfoPaperTouchTap: PropTypes.func,
    onModuleButtonTouchTap: PropTypes.func,
    onDeleteOkButtonTouchTap: PropTypes.func,
  }

  state = {
    deleteSchema: null,
    isIdCopiedSnackBarOpen: false,
    isSchemaDeleteDialogOpen: false,
  }

  /**
   * IDコピーボタン押下時の動作
   * @param {string} schemaId
   */
  onIdCopyButtonTouchTap(schemaId) {
    this.setState({
      isIdCopiedSnackBarOpen: true,
    })
  }

  /**
   * スナックバークローズ要求時の動作
   */
  onIdCopiedSnackBarCloseRequest() {
    this.setState({
      isIdCopiedSnackBarOpen: false,
    })
  }

  /**
   * 追加メニュー 削除の選択時の動作
   * @param {object} schema
   */
  onDeleteTouchTap(schema) {
    this.setState({
      deleteSchema: schema,
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
      deleteSchema: null,
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
      deleteSchema,
      isIdCopiedSnackBarOpen,
      isSchemaDeleteDialogOpen,
    } = this.state
    const {
      isFetching,
      schemas,
      modules,
      onSchemaInfoPaperTouchTap,
      onModuleButtonTouchTap,
    } = this.props

    if (isFetching) {
      return (
        <LoadingIndicator />
      )
    }

    return (
      <div className="page">
        {schemas.valueSeq().map((schema) =>
          <SchemaInfoPaper
            key={schema.uuid}
            schema={schema}
            modules={modules}
            onDisplayNameTouchTap={(schema) => onSchemaInfoPaperTouchTap(schema.uuid)}
            onIdCopyButtonTouchTap={::this.onIdCopyButtonTouchTap}
            onModuleButtonTouchTap={onModuleButtonTouchTap}
            onDeleteTouchTap={::this.onDeleteTouchTap}
          />
        )}

        <CCLink url={urls.schemasNew}>
          <AddFloatingActionButton />
        </CCLink>

        <Snackbar
          open={isIdCopiedSnackBarOpen}
          message="IDをコピーしました"
          autoHideDuration={4000}
          onRequestClose={::this.onIdCopiedSnackBarCloseRequest}
        />

        <SchemaDeleteDialog
          open={isSchemaDeleteDialogOpen}
          schema={deleteSchema}
          onOkTouchTap={(schema) => this.onDeleteDialogButtonTouchTap(true, schema)}
          onCancelTouchTap={() => this.onDeleteDialogButtonTouchTap(false)}
        />
      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  isFetching: state.asyncs.isSchemasFetching,
  schemas: state.entities.schemas,
  modules: state.entities.modules,
})

const mapDispatchToProps = (dispatch) => ({
  onSchemaInfoPaperTouchTap: (schemaId) => dispatch(routerActions.push(createPathName(urls.schema, {schemaId}))),
  onModuleButtonTouchTap: (moduleId) => dispatch(routerActions.push(createPathName(urls.module, {moduleId}))),
  onDeleteOkButtonTouchTap: (schema) => dispatch(actions.schemas.deleteRequest(schema.uuid)),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Schemas)
