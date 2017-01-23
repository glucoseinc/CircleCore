import {handleActions} from 'redux-actions'

import {actionTypes} from '../actions'

const initialState = {
  title: '',
}


const page = handleActions({
  [actionTypes.page.setTitle]: (state, action) => {
    const title = action.payload
    return {
      ...state,
      title,
    }
  },
}, initialState)

export default page
