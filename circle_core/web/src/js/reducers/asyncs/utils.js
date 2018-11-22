/**
 * 固定ステートに固定値をいれるActionのReducer
 * @param {str} stateName
 * @param {Object} newState
 * @return {Object} 新しいstate
 */
export function changeFlagAction(stateName, newState) {
  return (state, action) => {
    return Object.assign({}, state, {
      stateName: newState,
    })
  }
}
