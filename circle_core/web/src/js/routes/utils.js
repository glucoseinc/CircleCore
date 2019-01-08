import path from 'path'

import pathToRegexp from 'path-to-regexp'
import {matchPath} from 'react-router'

import rootRoute from './Root'


const createURLs = (route, parentPath = '') => {
  let urls = {}

  const fullPath = path.join(parentPath, route.path || '')

  if (route.key !== undefined) {
    urls[route.key] = {
      fullPath,
      query: route.query,
      label: route.label,
      icon: route.icon,
    }
  }
  if (route.childRoutes !== undefined) {
    urls = route.childRoutes.reduce((_urls, childRoute) => ({
      ..._urls,
      ...createURLs(childRoute, fullPath),
    }), urls)
  }

  return urls
}

export const urls = createURLs(rootRoute)

export const createPathName = (url, params) => {
  return pathToRegexp.compile(url.fullPath)(params)
}

export const createQuery = (url, params) => {
  if (url.query === undefined || params === undefined) {
    return null
  }

  return Object.entries(url.query).reduce((query, [key, value]) => {
    try {
      return {
        ...query,
        [key]: pathToRegexp.compile(value)(params),
      }
    } catch (e) {
      return query
    }
  }, {})
}

export const createSearchString = (url, params) => {
  const query = createQuery(url, params)
  return `?${Object.entries(query).map(([key, value]) => `${key}=${value}`).join('&')}`
}

export const searchStringToQuery = (searchString) => {
  return (
    searchString
      .replace(/^\?/, '')
      .split('&')
      .map((kv) => kv.split('='))
      .reduce(
        (prev, [key, value]) => ({
          ...prev,
          [key]: value,
        }),
        {},
      )
  )
}

const createFlatRoutes = (route, parentPath = '') => {
  const {
    childRoutes,
    path: routePath,
    ...other
  } = route

  let routes = []

  const fullPath = path.join(parentPath, routePath || '')

  if (route.key !== undefined) {
    routes.push({
      fullPath,
      ...other,
    })
  }
  if (childRoutes !== undefined) {
    routes = childRoutes.reduce((_routes, childRoute) => ([
      ..._routes,
      ...createFlatRoutes(childRoute, fullPath),
    ]), routes)
  }

  return routes
}

const flatRoutes = createFlatRoutes(rootRoute)

export const findRoute = (fullPath) => (
  flatRoutes.find((route) => (
    matchPath(
      fullPath,
      {
        path: route.fullPath,
        exact: true,
      },
    )
  ))
)

export const listUrls = (route, parentPath = '') => {
  let urls = []

  const fullPath = path.join(parentPath, route.path || '')

  if (route.childRoutes === undefined) {
    urls.push(fullPath)
  } else {
    urls = route.childRoutes.reduce((_urls, childRoute) => ([
      ..._urls,
      ...listUrls(childRoute, fullPath),
    ]), urls)
  }

  return urls
}
