export const createAsyncSagaParam = (api, apiParam, succeededAction, failedAction) => ({
  api,
  apiParam,
  succeededAction,
  failedAction,
})
