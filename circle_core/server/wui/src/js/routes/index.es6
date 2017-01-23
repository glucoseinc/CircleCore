import React from 'react'
import {Route, IndexRedirect} from 'react-router'

import rootRoute from './Root'
import Modules from './UserOnly/Master/Modules'

const defaultPage = Modules.path

const routes = (
  <Route {...rootRoute}>
    <IndexRedirect to={defaultPage} />
  </Route>
)

export default routes

export {urls, createPathName} from './utils'
