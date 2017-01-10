import React from 'react'

import Paper from 'material-ui/Paper'
import TextField from 'material-ui/TextField'

import {EditableActionsArea, NotEditableActionsArea, NullComponent} from './commons'


const EditableDisplayNameData = ({module, actions}) => (
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
)

const NotEditableDisplayNameData = ({module}) => (
  <td>{module.displayName}</td>
)


const ModuleGeneralInfo = ({editable, module, actions, hiddenUuid, hiddenActionsArea}) => {
  const DisplayNameData = editable ? EditableDisplayNameData : NotEditableDisplayNameData
  const ActionsArea = hiddenActionsArea ? NullComponent : (editable ? EditableActionsArea : NotEditableActionsArea)
  const UuidRow = hiddenUuid ? NullComponent : ({module}) => (
    <tr>
      <td>UUID</td>
      <td>{module.uuid}</td>
    </tr>
  )

  return (
    <Paper>
      <h3>General</h3>
      <table>
        <tbody>
          <tr>
            <td>Name</td>
            <DisplayNameData
              module={module}
              actions={actions}
            />
          </tr>
          <UuidRow
            module={module}
          />
        </tbody>
      </table>
      <ActionsArea
        editingArea="general"
        module={module}
        actions={actions}
      />
    </Paper>
  )
}

export default ModuleGeneralInfo
