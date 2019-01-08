import React from 'react'
import {Route, Redirect} from 'react-router-dom'

import rootRoute from './Root'
import modulesRoute from './UserOnly/Master/Modules'

const defaultPage = modulesRoute.path

const routes = (
  <Route {...rootRoute}>
    <Redirect from="/" to={defaultPage} />
  </Route>
)

export default routes

export {urls, createPathName, createQuery} from './utils'
