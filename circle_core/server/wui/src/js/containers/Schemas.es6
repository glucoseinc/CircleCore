import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'
import {routerActions} from 'react-router-redux'

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
    onIdCopyButtonTouchTap: PropTypes.func,
    onDeleteOkButtonTouchTap: PropTypes.func,
  }

  state = {
    deleteSchema: null,
    isSchemaDeleteDialogOpen: false,
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
      isSchemaDeleteDialogOpen,
    } = this.state
    const {
      isFetching,
      schemas,
      modules,
      onSchemaInfoPaperTouchTap,
      onModuleButtonTouchTap,
      onIdCopyButtonTouchTap,
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
            onIdCopyButtonTouchTap={onIdCopyButtonTouchTap}
            onModuleButtonTouchTap={onModuleButtonTouchTap}
            onDeleteTouchTap={::this.onDeleteTouchTap}
          />
        )}

        <CCLink url={urls.schemasNew}>
          <AddFloatingActionButton />
        </CCLink>

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
  onIdCopyButtonTouchTap: (uuid) => dispatch(actions.page.showSnackbar('IDをコピーしました')),
  onDeleteOkButtonTouchTap: (schema) => dispatch(actions.schemas.deleteRequest(schema.uuid)),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Schemas)
