import path from 'path'
import React from 'react'
import {Route, IndexRedirect} from 'react-router'

import Master from '../containers/Master'
import {GuestOnly, UserOnly} from '../containers/AuthDivider'
import OAuthAuthorize from '../containers/OAuthAuthorize'
import NotFound from '../components/NotFound'
import pages, {defaultPage} from './pages'


const rootRoute = (
  <Route path="/">
    <Route component={UserOnly}>
      <Route component={Master}>
        <IndexRedirect to={defaultPage.path} />
        <Route childRoutes={pages} />
      </Route>
    </Route>
    <Route component={GuestOnly}>
      <Route path="/oauth/authorize" component={OAuthAuthorize} />
      <Route path="/oauth/callback" component={() => <div>Checking AuthCode...</div>} />
    </Route>
    <Route path="*" component={NotFound} />
  </Route>
)


export default rootRoute


const createURLs = (route, parentPath = '') => {
  let urls = {}

  if (route.key !== undefined) {
    urls[route.key] = {
      fullPath: path.join(parentPath, route.path),
      label: route.label,
      icon: route.icon,
    }
  }
  if (route.childRoutes !== undefined) {
    urls = route.childRoutes.reduce((_urls, childRoute) => ({
      ..._urls,
      ...createURLs(childRoute, route.path),
    }), urls)
  }

  return urls
}
const urls = pages.reduce((urls, childRoute) => ({
  ...urls,
  ...createURLs(childRoute, '/'),
}), {})
urls.root = {
  fullPath: '/',
  label: 'CircleCore',
}
export {urls}
