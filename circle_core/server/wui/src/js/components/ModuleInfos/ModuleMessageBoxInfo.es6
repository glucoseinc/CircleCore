import React from 'react'

import MenuItem from 'material-ui/MenuItem'
import Paper from 'material-ui/Paper'
import RaisedButton from 'material-ui/RaisedButton'
import SelectField from 'material-ui/SelectField'
import TextField from 'material-ui/TextField'

import {EditableActionsArea, NotEditableActionsArea, NullComponent} from './commons'


const EditableDisplayNameData = ({module, index, actions}) => {
  const messageBox = module.messageBoxes.get(index)
  return (
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
  )
}

const NotEditableDisplayNameData = ({module, index}) => {
  const messageBox = module.messageBoxes.get(index)
  return (
    <td>{messageBox.displayName}</td>
  )
}

const EditableSchemaData = ({module, index, schemas, actions}) => {
  const messageBox = module.messageBoxes.get(index)
  const schema = schemas.get(messageBox.schema)
  return (
    <td>
      <SelectField
        value={messageBox.schema}
        onChange={(e, i, v) => actions.module.update(
          module.updateMessageBox(index, 'schema', v)
        )}
      >
        {schemas.valueSeq().map((schema) =>
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
          {schema ? schema.properties.map((property, i) =>
            <tr key={i}>
              <td>{property.name}</td>
              <td>{property.type}</td>
            </tr>
          ) : null}
        </tbody>
      </table>
    </td>
  )
}

const NotEditableSchemaData = ({module, index, schemas}) => {
  const messageBox = module.messageBoxes.get(index)
  const schema = schemas.get(messageBox.schema)
  return (
    <td>
      {schema.label}
      <table>
        <thead>
          <tr>
            <th colSpan={2}>Properties</th>
          </tr>
        </thead>
        <tbody>
          {schema.properties.map((property, i) =>
              <tr key={i}>
                <td>{property.name}</td>
                <td>{property.type}</td>
              </tr>
            )
          }
        </tbody>
      </table>
    </td>
  )
}

const EditableMemoData = ({module, index, actions}) => {
  const messageBox = module.messageBoxes.get(index)
  return (
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
  )
}

const NotEditableMemoData = ({module, index, actions}) => {
  const messageBox = module.messageBoxes.get(index)
  return (
    <td>{messageBox.description}</td>
  )
}


const MessageBoxInfo = ({editable, module, index, schemas, actions}) => {
  const DisplayNameData = editable ? EditableDisplayNameData : NotEditableDisplayNameData
  const SchemaData = editable ? EditableSchemaData : NotEditableSchemaData
  const MemoData = editable ? EditableMemoData : NotEditableMemoData
  const DeleteButton = editable ? ({module, index, actions}) => (
    <RaisedButton
      label="Delete this Message box"
      secondary={true}
      onTouchTap={() => actions.module.update(
        module.removeMessageBox(index)
      )}
    />
  ) : NullComponent

  return (
    <Paper>
      <table>
        <tbody>
          <tr>
            <td>Name</td>
            <DisplayNameData
              module={module}
              index={index}
              actions={actions}
            />
          </tr>
          <tr>
            <td>Message schema</td>
            <SchemaData
              module={module}
              index={index}
              schemas={schemas}
              actions={actions}
            />
          </tr>
          <tr>
            <td>memo</td>
            <MemoData
              module={module}
              index={index}
              actions={actions}
            />
          </tr>
        </tbody>
      </table>
      <DeleteButton
        module={module}
        index={index}
        actions={actions}
      />
    </Paper>
  )
}

const ModuleMessageBoxesInfo = ({editable, module, schemas, actions, hiddenActionsArea}) => {
  const NewMessageButton = editable ? ({module, actions}) => (
    <RaisedButton
      label="Add New Message box"
      primary={true}
      onTouchTap={() => actions.module.update(
        module.pushMessageBox()
      )}
    />
  ) : NullComponent
  const ActionsArea = hiddenActionsArea ? NullComponent : (editable ? EditableActionsArea : NotEditableActionsArea)
  return (
    <Paper>
      <h3>Message box</h3>
      {module.messageBoxes.map((messageBox, index) =>
        <MessageBoxInfo
          key={index}
          editable={editable}
          module={module}
          index={index}
          schemas={schemas}
          actions={actions}
        />
      )}
      <NewMessageButton
        module={module}
        actions={actions}
      />
      <ActionsArea
        editingArea="messageBox"
        module={module}
        actions={actions}
      />
    </Paper>
  )
}

export default ModuleMessageBoxesInfo
