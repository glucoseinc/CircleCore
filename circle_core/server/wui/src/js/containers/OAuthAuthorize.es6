import React from 'react'

/**
 * /oauth/authorizeにアクセスされたら呼ばれる。 このページはWebサーバ側でレンダリングするので、ReloadしてReactから抜ける...
 * @return {React.Component}
 */
export default function OAuthAuthorize() {
  location.reload()
  return <div>Redirecting...</div>
}
