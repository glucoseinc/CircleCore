import {createAction} from 'redux-actions'

import actionTypes from '../constants/ActionTypes'


export default {
  searchTextChange: createAction(actionTypes.miscs.searchTextChange),
  tagTouchTap: createAction(actionTypes.modules.filterByTag),
  deleteTouchTap: createAction(actionTypes.module.deleteAsked),
  deleteExecuteTouchTap: createAction(actionTypes.module.deleteRequested),
  deleteCancelTouchTap: createAction(actionTypes.module.deleteCanceled, () => null),
}
