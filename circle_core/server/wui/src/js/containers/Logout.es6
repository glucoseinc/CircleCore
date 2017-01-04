import {connect} from 'react-redux'
import {logout} from '../Authorization'

/**
 * ログアウトする
 */
export default connect()(() => {
  logout()
  return <div />
})
