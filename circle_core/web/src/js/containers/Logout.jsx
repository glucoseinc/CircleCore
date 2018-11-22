import React from 'react'
import {connect} from 'react-redux'
import {logout} from 'src/Authorization'


/**
 * ログアウトする
 */
export default connect()(() => {
  logout()
  return <div />
})
