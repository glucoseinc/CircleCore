import {Map} from 'immutable'
import {normalize} from 'normalizr'

import {actionTypes} from 'src/actions'
import User from 'src/models/User'
import normalizerSchema from 'src/models/normalizerSchema'

import {convertValues} from './utils'


const usersActionsHandler = {
  [actionTypes.users.fetchComplete]: (state, {payload: {response, error}}) => {
    if(response) {
      const {entities} = normalize(response, normalizerSchema)
      const users = new Map(convertValues(entities.users, User.fromObject))

      return {...state, users}
    }
    return state
  },

  [actionTypes.users.deleteComplete]: (state, {payload: {response, error}}) => {
    if(response) {
      // 削除されるUserはたかだか1個なのでこの実装で問題ないと思う
      const {entities} = normalize(response, normalizerSchema)
      let users = state.users
      Object.entries(entities.users).forEach(([uuid, obj]) => {
        users = users.delete(uuid)
      })
      return {...state, users}
    }
    return state
  },

  [actionTypes.user.updateComplete]: (state, {payload: {response, error}}) => {
    if(response) {
      const {entities} = normalize(response, normalizerSchema)
      const users = state.users.merge(
        new Map(convertValues(entities.users, User.fromObject))
      )
      return {...state, users}
    }
    return state
  },

  [actionTypes.users.fetchMeComplete]: (state, {payload: {response, error}}) => {
    if(response) {
      const normalized = normalize(response, normalizerSchema)
      const users = state.users.merge(
        new Map(convertValues(normalized.entities.users, User.fromObject))
      )

      return {...state, users, myID: normalized.result.user}
    } else {
      return {...state, myID: null}
    }
  },

}

export default usersActionsHandler
