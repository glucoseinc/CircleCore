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
    <Route path="modules" component={require('./pages/ModuleList').default}>
    </Route>
    <Route path="/module/:moduleId" component={require('./pages/ModulePage').default} />

    <Route path="*" component={() => (<div>Page not found</div>)}/>
  </Route>
)
export default AppRoutes

