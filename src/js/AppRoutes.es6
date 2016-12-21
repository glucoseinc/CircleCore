import React from 'react'
import {
  Route,
  // Redirect,
  IndexRoute,
} from 'react-router'

import Master from './components/Master'
import HomePage from './pages/Home'


const AppRoutes = (
  <Route path="/" component={Master}>
    <IndexRoute component={HomePage} />
    <Route path="home" component={HomePage} />
  </Route>
)
export default AppRoutes

