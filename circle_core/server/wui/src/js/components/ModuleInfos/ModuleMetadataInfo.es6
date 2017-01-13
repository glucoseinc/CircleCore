import React from 'react'

import Chip from 'material-ui/Chip'
import Paper from 'material-ui/Paper'
import TextField from 'material-ui/TextField'

import {EditableActionsArea, NotEditableActionsArea, NullComponent} from './commons'


const EditableTagData = ({module, inputText, actions}) => (
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
)

const NotEditableTagData = ({module}) => (
  <td>
    {module.tags.map((tag, index) =>
      <Chip key={index}>{tag}</Chip>
    )}
  </td>
)

const EditableMemoData = ({module, actions}) => (
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
)

const NotEditableMemoData = ({module, actions}) => (
  <td>{module.description}</td>
)


const ModuleMetadataInfo = ({editable, module, inputText, actions, hiddenActionsArea}) => {
  const TagData = editable ? EditableTagData : NotEditableTagData
  const MemoData = editable ? EditableMemoData : NotEditableMemoData
  const ActionsArea = hiddenActionsArea ? NullComponent : (editable ? EditableActionsArea : NotEditableActionsArea)
  return (
    <Paper>
      <h3>Metadata</h3>
      <table>
        <tbody>
          <tr>
            <td>Tag</td>
            <TagData
              module={module}
              inputText={inputText}
              actions={actions}
            />
          </tr>
          <tr>
            <td>memo</td>
            <MemoData
              module={module}
              actions={actions}
            />
          </tr>
        </tbody>
      </table>
      <ActionsArea
        editingArea="metadata"
        module={module}
        actions={actions}
      />
    </Paper>
  )
}

export default ModuleMetadataInfo
