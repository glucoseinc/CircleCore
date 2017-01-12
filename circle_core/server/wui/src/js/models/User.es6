/* eslint-disable new-cap */
import {Record} from 'immutable'


const UserRecord = Record({
  uuid: '',
  // schema: new Schema(),
  // displayName: '',
  // description: '',
})

/**
 */
export default class User extends UserRecord {
  /**
   * @override
   */
  constructor(...args) {
    super(...args)
  }

  /**
   * @param {object} rawUser
   * @return {User}
   */
  static fromObject(rawUser) {
    return new User({
      uuid: rawUser.uuid,
      // schema: Schema.fromObject(rawMessageBox.schema || {}),
      // displayName: rawMessageBox.displayName || '',
      // description: rawMessageBox.description || '',
    })
  }
}
