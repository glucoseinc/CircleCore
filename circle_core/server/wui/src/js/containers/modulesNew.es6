import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'

import Chip from 'material-ui/Chip'
import MenuItem from 'material-ui/MenuItem'
import Paper from 'material-ui/Paper'
import RaisedButton from 'material-ui/RaisedButton'
import SelectField from 'material-ui/SelectField'
import TextField from 'material-ui/TextField'

import actions from '../actions'
import {urls} from '../routes'
import CCLink from '../components/CCLink'
import Fetching from '../components/Fetching'


/**
 */
class ModulesNew extends Component {
  static propTypes = {
    isSchemasFetching: PropTypes.bool.isRequired,
    schemas: PropTypes.array.isRequired,
    module: PropTypes.object.isRequired,
    inputText: PropTypes.string.isRequired,
    actions: PropTypes.object.isRequired,
  }

  /**
   * @override
   */
  componentWillMount() {
    const {
      actions,
    } = this.props
    actions.module.createInit()
    actions.schemas.fetchRequest()
  }


  /**
   * @override
   */
  render() {
    const {
      isSchemasFetching,
      schemas,
      module,
      inputText,
      actions,
    } = this.props

    if (isSchemasFetching) {
      return (
        <Fetching />
      )
    }

    return (
      <div>
        <Paper>
          <h3>General</h3>
          <table>
            <tbody>
              <tr>
                <td>Name</td>
                <td>
                  <TextField
                    name="displayName"
                    hintText="Option"
                    fullWidth={true}
                    value={module.displayName}
                    onChange={(e) => actions.module.update(
                      module.update('displayName', e.target.value)
                    )}
                  />
                </td>
              </tr>
            </tbody>
          </table>
        </Paper>
        <Paper>
          <h3>Message box</h3>
          {module.messageBoxes.map((messageBox, index) =>
            <Paper key={index}>
              <table>
                <tbody>
                  <tr>
                    <td>Name</td>
                    <td>
                      <TextField
                        name="displayName"
                        hintText="Option"
                        fullWidth={true}
                        value={messageBox.displayName}
                        onChange={(e) => actions.module.update(
                          module.updateMessageBox(index, 'displayName', e.target.value)
                        )}
                      />
                    </td>
                  </tr>
                  <tr>
                    <td>Message schema</td>
                    <td>
                      <SelectField
                        value={messageBox.schema.uuid}
                        onChange={(e, i, v) => {
                          const schema = schemas.find((_schema) => _schema.uuid === v)
                          actions.module.update(
                            module.updateMessageBox(index, 'schema', schema)
                          )
                        }}
                      >
                        {schemas.map((schema) =>
                          <MenuItem
                            key={schema.uuid}
                            value={schema.uuid}
                            label={schema.label}
                            primaryText={schema.label}
                          />
                        )}
                      </SelectField>
                      <table>
                        <thead>
                          <tr>
                            <th colSpan={2}>Properties</th>
                          </tr>
                        </thead>
                        <tbody>
                          {messageBox.schema.properties.map((property, i) =>
                            <tr key={i}>
                              <td>{property.name}</td>
                              <td>{property.type}</td>
                            </tr>
                          )}
                        </tbody>
                      </table>
                    </td>
                  </tr>
                  <tr>
                    <td>memo</td>
                    <td>
                      <TextField
                        name="memo"
                        hintText="Option"
                        fullWidth={true}
                        multiLine={true}
                        rows={4}
                        rowsMax={4}
                        value={messageBox.description}
                        onChange={(e) => actions.module.update(
                          module.updateMessageBox(index, 'description', e.target.value)
                        )}
                      />
                    </td>
                  </tr>
                </tbody>
              </table>
              <RaisedButton
                label="Delete this Message box"
                secondary={true}
                onTouchTap={() => actions.module.update(
                  module.removeMessageBox(index)
                )}
              />
            </Paper>
          )}
          <RaisedButton
            label="Add New Message box"
            primary={true}
            onTouchTap={() => actions.module.update(
              module.pushMessageBox()
            )}
          />

        </Paper>
        <Paper>
          <h3>Metadata</h3>
          <table>
            <tbody>
              <tr>
                <td>Tag</td>
                <td>
                {module.tags.map((tag, index) =>
                  <Chip
                    key={index}
                    onRequestDelete={() => {
                      actions.module.update(
                        module.removeTag(index)
                      )
                    }}
                  >
                    {tag}
                  </Chip>
                )}
                <TextField
                  hintText="Add new tag"
                  value={inputText}
                  onChange={(e) => actions.misc.inputTextChange(e.target.value)}
                  onKeyUp={(e) => {
                    if (e.keyCode === 13) {
                      actions.module.update(
                        module.pushTag(inputText)
                      )
                      actions.misc.inputTextChange('')
                    }
                  }}
                />
                </td>
              </tr>
              <tr>
                <td>memo</td>
                <td>
                  <TextField
                    name="memo"
                    hintText="Option"
                    fullWidth={true}
                    multiLine={true}
                    rows={4}
                    rowsMax={4}
                    value={module.description}
                    onChange={(e) => actions.module.update(
                      module.update('description', e.target.value)
                    )}
                  />
                </td>
              </tr>
            </tbody>
          </table>
        </Paper>
        <CCLink
          url={urls.modules}
        >
          <RaisedButton
            label="Cancel"
            secondary={true}
          />
        </CCLink>
        <RaisedButton
          label="Create"
          primary={true}
          disabled={module.isReadytoCreate() ? false : true}
          onTouchTap={() => actions.modules.createRequest(module)}
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
    isSchemasFetching: state.asyncs.isSchemasFetching,
    schemas: state.entities.schemas,
    module: state.misc.module,
    inputText: state.misc.inputText,
  }
}

/**
 * [mapDispatchToProps description]
 * @param  {[type]} dispatch [description]
 * @return {[type]}          [description]
 */
function mapDispatchToProps(dispatch) {
  return {
    actions: {
      schemas: bindActionCreators(actions.schemas, dispatch),
      modules: bindActionCreators(actions.modules, dispatch),
      module: bindActionCreators(actions.module, dispatch),
      misc: bindActionCreators(actions.misc, dispatch),
    },
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(ModulesNew)
