/**
 * 例外オブジェから、Actionの返り値用のErrorを作り直す
 * @param {Error} e
 * @return {Error} new error
 */
export function makeError(e) {
  let msg = (e.response && e.response.body && e.response.body.detail && e.response.body.detail.reason) || e.message
  return new Error(msg)
}
