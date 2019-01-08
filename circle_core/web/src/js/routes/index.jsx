import path from 'path'

import React from 'react'
import {Switch, Redirect, Route} from 'react-router-dom'

import rootRoute from './Root'
import modulesRoute from './UserOnly/Master/Modules'
import {listUrls, findRoute, urls} from './utils'

const defaultPage = urls[modulesRoute.key].fullPath

// eslint-disable-next-line react/display-name
const renderRoute = (parentPath) => (route) => (
  <Route
    exact
    key={route.key}
    path={listUrls(route, parentPath)}
    render={(props) => {
      const Component = route.component
      const matchedRoute = findRoute(props.location.pathname)
      if (route.childRoutes) {
        return (
          <Component {...props} route={matchedRoute}>
            <Switch>
              {route.childRoutes.map(renderRoute(path.join(parentPath, route.path || '')))}
            </Switch>
          </Component>
        )
      }
      return (
        <Component {...props} route={matchedRoute} />
      )
    }}
  />
)

const Routes = () => (
  <Switch>
    <Redirect exact from={rootRoute.path} to={defaultPage} />
    {rootRoute.childRoutes.map(renderRoute(rootRoute.path))}
  </Switch>
)

export default Routes

export {urls, createPathName, createQuery, createSearchString, searchStringToQuery} from './utils'
