import path from 'path'

import pathToRegexp from 'path-to-regexp'

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
