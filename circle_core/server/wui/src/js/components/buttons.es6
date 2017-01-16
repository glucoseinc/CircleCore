import React from 'react'

import RaisedButton from 'material-ui/RaisedButton'
import ContentAdd from 'material-ui/svg-icons/content/add'
import ContentRemove from 'material-ui/svg-icons/content/remove'

const nullFunctoin = () => null

export const AddButton = (props) => {
  const {
    label = '追加する',
    disabled = false,
    onTouchTap = nullFunctoin,
  } = props

  return (
    <RaisedButton
      label={label}
      primary={true}
      icon={<ContentAdd />}
      disabled={disabled}
      onTouchTap={onTouchTap}
    />
  )
}

export const BackButton = (props) => {
  const {
    label = '戻る',
    disabled = false,
    onTouchTap = nullFunctoin,
  } = props

  return (
    <RaisedButton
      label={label}
      disabled={disabled}
      onTouchTap={onTouchTap}
    />
  )
}

export const CancelButton = (props) => {
  const {
    label = 'キャンセル',
    disabled = false,
    onTouchTap = nullFunctoin,
  } = props

  return (
    <RaisedButton
      label={label}
      secondary={true}
      disabled={disabled}
      onTouchTap={onTouchTap}
    />
  )
}

export const CreateButton = (props) => {
  const {
    label = '作成する',
    disabled = false,
    onTouchTap = nullFunctoin,
  } = props

  return (
    <RaisedButton
      label={label}
      primary={true}
      disabled={disabled}
      onTouchTap={onTouchTap}
    />
  )
}

export const EditButton = (props) => {
  const {
    label = '編集する',
    disabled = false,
    onTouchTap = nullFunctoin,
  } = props

  return (
    <RaisedButton
      label={label}
      primary={true}
      disabled={disabled}
      onTouchTap={onTouchTap}
    />
  )
}

export const RemoveButton = (props) => {
  const {
    label = '削除する',
    disabled = false,
    onTouchTap = nullFunctoin,
  } = props

  return (
    <RaisedButton
      label={label}
      secondary={true}
      disabled={disabled}
      icon={<ContentRemove />}
      onTouchTap={onTouchTap}
    />
  )
}

export const UpdateButton = (props) => {
  const {
    label = '更新する',
    disabled = false,
    onTouchTap = nullFunctoin,
  } = props

  return (
    <RaisedButton
      label={label}
      primary={true}
      disabled={disabled}
      onTouchTap={onTouchTap}
    />
  )
}

