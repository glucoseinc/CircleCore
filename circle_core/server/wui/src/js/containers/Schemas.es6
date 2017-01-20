import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'
import {routerActions} from 'react-router-redux'

import actions from '../actions'
import {FloatingAddButton} from '../components/buttons'
import CCLink from '../components/CCLink'
import Fetching from '../components/Fetching'
import SchemaDeleteDialog from '../components/SchemaDeleteDialog'
import SchemaInfoPaper from '../components/SchemaInfoPaper'
import {urls, createPathName} from '../routes'


/**
 * Schema一覧
 */
class Schemas extends Component {
  static propTypes = {
    isFetching: PropTypes.bool.isRequired,
    schemas: PropTypes.object.isRequired,
    modules: PropTypes.object.isRequired,
    onModuleButtonTouchTap: PropTypes.func,
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
  componentWillMount() {
    const {
      actions,
    } = this.props
    actions.schemas.fetchRequest()
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
      onModuleButtonTouchTap,
    } = this.props

    if (isFetching) {
      return (
        <Fetching />
      )
    }

    return (
      <div>
        {schemas.valueSeq().map((schema) => (
          <SchemaInfoPaper
            key={schema.uuid}
            schema={schema}
            modules={modules}
            onModuleButtonTouchTap={onModuleButtonTouchTap}
            onDeleteTouchTap={::this.onDeleteTouchTap}
          />
        ))}

        <CCLink url={urls.schemasNew}>
          <FloatingAddButton />
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
  onModuleButtonTouchTap: (moduleId) => dispatch(routerActions.push(createPathName(urls.module, {moduleId}))),
  onDeleteOkButtonTouchTap: (schema) => dispatch(actions.schemas.deleteRequest(schema)),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(Schemas)
