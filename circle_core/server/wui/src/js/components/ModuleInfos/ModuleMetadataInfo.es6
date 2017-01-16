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
      hintText="タグを追加"
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

const NotEditableTagData = ({module}) => {
  const style = {
    tags: {
      display: 'flex',
    },
    tag: {
      margin: 4,
    },
  }
  return (
    <td>
      <div style={style.tags}>
        {module.tags.map((tag, index) =>
          <Chip
            key={index}
            style={style.tag}>
            {tag}
          </Chip>
        )}
      </div>
    </td>
  )
}

const EditableMemoData = ({module, actions}) => (
  <td>
    <TextField
      name="memo"
      hintText="オプション"
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
      <p>メタデータ</p>
      <table className="props">
        <tbody>
          <tr>
            <th>タグ</th>
            <TagData
              module={module}
              inputText={inputText}
              actions={actions}
            />
          </tr>
          <tr>
            <th>メモ</th>
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
