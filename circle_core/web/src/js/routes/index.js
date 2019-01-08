import React from 'react'
import {Route, IndexRedirect} from 'react-router'

import rootRoute from './Root'
import modulesRoute from './UserOnly/Master/Modules'

const defaultPage = modulesRoute.path

const routes = (
  <Route {...rootRoute}>
    <IndexRedirect to={defaultPage} />
  </Route>
)

export default routes

export {urls, createPathName, createQuery} from './utils'
