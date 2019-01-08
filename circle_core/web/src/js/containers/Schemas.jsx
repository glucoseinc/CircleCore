import {routerActions} from 'connected-react-router'
import PropTypes from 'prop-types'
import React from 'react'
import {connect} from 'react-redux'

import actions from 'src/actions'
import {urls, createPathName, createQuery} from 'src/routes'

import LoadingIndicator from 'src/components/bases/LoadingIndicator'
import {SchemaIcon} from 'src/components/bases/icons'

import AddFloatingActionButton from 'src/components/commons/AddFloatingActionButton'
import CCLink from 'src/components/commons/CCLink'
import SchemaDeleteDialog from 'src/components/commons/SchemaDeleteDialog'

import Empty from 'src/components/Empty'
import SchemaInfoPaper from 'src/components/SchemaInfoPaper'


/**
 * Schema一覧
 */
class Schemas extends React.Component {
  static propTypes = {
    isSchemaFetching: PropTypes.bool.isRequired,
    isCcInfoFetching: PropTypes.bool.isRequired,
    schemas: PropTypes.object.isRequired,
    modules: PropTypes.object.isRequired,
    ccInfos: PropTypes.object.isRequired,
    onDisplayNameClick: PropTypes.func,
    onModuleButtonClick: PropTypes.func,
    onTemplateClick: PropTypes.func,
    onDeleteOkButtonClick: PropTypes.func,
  }

  state = {
    deleteSchema: null,
    isSchemaDeleteDialogOpen: false,
  }

  /**
   * 追加メニュー 削除の選択時の動作
   * @param {object} schema
   */
  onDeleteClick(schema) {
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
  onDeleteDialogButtonClick(execute, schema) {
    this.setState({
      deleteSchema: null,
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
      deleteSchema,
      isSchemaDeleteDialogOpen,
    } = this.state
    const {
      isSchemaFetching,
      isCcInfoFetching,
      schemas,
      modules,
      ccInfos,
      onDisplayNameClick,
      onModuleButtonClick,
      onTemplateClick,
    } = this.props

    if (isSchemaFetching || isCcInfoFetching) {
      return (
        <LoadingIndicator />
      )
    }

    const ownCcInfo = ccInfos.filter((ccInfo) => ccInfo.myself).first()

    return (
      <div>
        {schemas.size === 0 ? (
          <Empty
            icon={SchemaIcon}
            itemName="メッセージスキーマ"
          />
        ) : (
          <div className="page">
            {schemas.valueSeq().map((schema) => (
              <SchemaInfoPaper
                key={schema.uuid}
                schema={schema}
                modules={modules}
                ownCcInfo={ownCcInfo}
                onDisplayNameClick={(schema) => onDisplayNameClick(schema.uuid)}
                onModuleButtonClick={onModuleButtonClick}
                onTemplateClick={(shcmea) => onTemplateClick(schema.uuid)}
                onDeleteClick={::this.onDeleteClick}
              />
            ))}
          </div>
        )}

        <CCLink url={urls.schemasNew}>
          <AddFloatingActionButton />
        </CCLink>

        <SchemaDeleteDialog
          open={isSchemaDeleteDialogOpen}
          schema={deleteSchema}
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
  modules: state.entities.modules,
  ccInfos: state.entities.ccInfos,
})

const mapDispatchToProps = (dispatch) => ({
  onDisplayNameClick: (schemaId) => dispatch(routerActions.push(createPathName(urls.schema, {schemaId}))),
  onModuleButtonClick: (moduleId) => dispatch(routerActions.push(createPathName(urls.module, {moduleId}))),
  onTemplateClick: (schemaId) => dispatch(routerActions.push({
    pathname: createPathName(urls.schemasNew),
    query: createQuery(urls.schemasNew, {schemaId}),
  })),
  onDeleteOkButtonClick: (schema) => dispatch(actions.schema.deleteRequest(schema.uuid)),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Schemas)
