import React from 'react'

import RaisedButton from 'material-ui/RaisedButton'


export const EditableActionsArea = ({module, actions}) => (
  <div>
    <RaisedButton
      label="Cancel"
      secondary={true}
      onTouchTap={actions.misc.cancelModuleEdit}
    />
    <RaisedButton
      label="Update"
      primary={true}
      onTouchTap={() => actions.misc.executeModuleEdit(module)}
    />
  </div>
)

export const NotEditableActionsArea = ({module, editingArea, actions}) => (
  <RaisedButton
    label="Edit"
    primary={true}
    onTouchTap={() => actions.misc.startModuleEdit({
      module,
      editingArea,
    })}
  />
)

export const NullComponent = () => null
