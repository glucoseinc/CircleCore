import React from 'react'

import {CancelButton, EditButton, UpdateButton} from '../../components/buttons'

export const EditableActionsArea = ({module, actions}) => (
  <div>
    <CancelButton
      onTouchTap={actions.misc.cancelModuleEdit}
    />
    <UpdateButton
      onTouchTap={() => actions.misc.executeModuleEdit(module)}
    />
  </div>
)

export const NotEditableActionsArea = ({module, editingArea, actions}) => (
  <EditButton
    onTouchTap={() => actions.misc.startModuleEdit({
      module,
      editingArea,
    })}
  />
)

export const NullComponent = () => null
